import datetime

from django.db.models import Count, Q
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from quiz.models import Tag, Quiz, QuizAnswer
from quiz.api.serializers import TagSerializer, QuizSerializer, QuizAnswerSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class QuizViewSet(ModelViewSet):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(created_by=user).prefetch_related('choices')

    @action(methods=['GET'], detail=False)
    def random(self, request):
        limit = int(request.GET.get('limit')) if request.GET.get('limit') is not None else 10
        quiz = self.queryset.random(self.request.user, limit)

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

    def create(self, request, *args, **kwargs):
        pk = request.data['quiz_id'] or 0
        quiz = get_object_or_404(Quiz.objects.prefetch_related('choices'), pk=pk)
        quiz_choices = quiz.choices.all()

        choices = []
        for choice in quiz_choices:
            is_select = choice.id in request.data['choices']
            choice = {
                'choice': choice.sentence,
                'is_answer': choice.is_answer,
                'is_select': is_select,
            }
            choices.append(choice)

        payload = {
            'account_id': self.request.user.id,
            'quiz_id': quiz.id,
            'question': quiz.question,
            'is_correct': request.data['is_correct'],
            'answer_choices': choices
        }
        serializer = QuizAnswerSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
