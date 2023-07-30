from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from account.api.serializers import AccountSerializer
from quiz.models import Tag, Quiz, QuizChoice, QuizTag, QuizAnswer, QuizAnswerChoice


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class QuizSerializer(serializers.ModelSerializer):
    question = serializers.CharField()
    is_published = serializers.BooleanField()
    is_deleted = serializers.BooleanField()
    choices = SerializerMethodField()
    tags = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = '__all__'

    @staticmethod
    def get_choices(obj):
        return QuizChoiceSerializer(QuizChoice.objects.all().filter(quiz_id=obj.id), many=True).data

    @staticmethod
    def get_tags(obj):
        quiz = Quiz.objects.get(pk=obj.pk)
        serializer = TagSerializer(quiz.tags.all(), many=True)
        return serializer.data

    @staticmethod
    def get_created_by(obj):
        quiz = Quiz.objects.get(pk=obj.pk)
        serializer = AccountSerializer(quiz.created_by)
        return serializer.data


class QuizChoiceSerializer(serializers.ModelSerializer):
    sentence = serializers.CharField()
    is_answer = serializers.BooleanField()
    sort = serializers.IntegerField()

    class Meta:
        model = QuizChoice
        fields = '__all__'


class QuizAnswerSerializer(serializers.ModelSerializer):
    answer_choices = SerializerMethodField()

    class Meta:
        model = QuizAnswer
        fields = '__all__'

    @staticmethod
    def get_answer_choices(obj):
        return QuizAnswerChoiceSerializer(QuizAnswerChoice.objects.filter(answer_id=obj.id).all(), many=True).data


class QuizAnswerChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswerChoice
        fields = '__all__'
