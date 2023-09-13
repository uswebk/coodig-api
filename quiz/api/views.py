import datetime

from django.db import transaction
from django.db.models import Count, Q
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from quiz.models import Tag, Quiz, QuizAnswer
from quiz.api.serializers import TagSerializer, QuizSerializer, QuizAnswerSerializer
from quiz.services import AnswerService, QuizService, RandomQuizServie


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class QuizViewSet(ModelViewSet):
    serializer_class = QuizSerializer

    def get_queryset(self):
        user = self.request.user
        return Quiz.objects.filter(created_by=user).prefetch_related('choices')

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            account = self.request.user
            data = request.data['quiz']
            data['created_by'] = account.id
            quiz_serializer = self.get_serializer(data=data)
            quiz_serializer.is_valid(raise_exception=True)
            quiz = quiz_serializer.save()

            quiz_service = QuizService(quiz)
            quiz_service.create_choices(request.data['quiz']['choices'])
            quiz_service.create_tags(request.data['tags'], account)

        return Response(quiz_serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, pk=None):
        quiz = get_object_or_404(Quiz, pk=pk, created_by=self.request.user, is_deleted=False)
        quiz.is_deleted = True
        quiz.save()
        return Response({}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def answer(self, request, pk=None):
        quiz = get_object_or_404(Quiz.objects.prefetch_related('choices'), pk=pk)

        # TODO: check already answered

        answer_service = AnswerService(quiz, self.request.user)
        answer_serializer = answer_service.create_answer(request.data['is_correct'])
        answer_service.create_answer_choices(quiz, request.data['choices'])

        return Response(answer_serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=False)
    def random(self, request):
        limit = int(request.GET.get('limit')) if request.GET.get('limit') is not None else 10
        quiz = RandomQuizServie.get_random(self.request.user, limit)

        if not quiz:
            raise Http404
        return Response(self.serializer_class(quiz, many=True).data, status=status.HTTP_200_OK)


class AnswerViewSet(ModelViewSet):
    serializer_class = QuizAnswerSerializer

    def get_queryset(self):
        account = self.request.user
        queryset = QuizAnswer.objects.filter(account_id=account.id).prefetch_related('answer_choices')

        start_date = self.request.query_params.get('start_date')
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)

        end_date = self.request.query_params.get('end_date')
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset

    @action(methods=['GET'], detail=False)
    def stats(self, request):
        now = datetime.datetime.now(datetime.timezone.utc)
        account = self.request.user
        result = QuizAnswer.objects.filter(account_id=account).values('account_id').aggregate(
            quiz_count=Count('id'),
            correct_count=Count('id', filter=Q(is_correct=True)),
            today_answer_count=Count('id', filter=Q(created_at__date=now)),
            today_correct_count=Count('id', filter=Q(created_at__date=now, is_correct=True)),
        )
        quiz_count = Quiz.objects.filter(is_published=True, is_deleted=False).aggregate(count=Count('id'))
        result['total'] = quiz_count['count']

        return Response(result)
