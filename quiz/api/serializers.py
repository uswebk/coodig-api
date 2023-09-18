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


class QuizAnswerChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswerChoice
        fields = '__all__'
        read_only_fields = ('answer_id',)


class QuizAnswerSerializer(serializers.ModelSerializer):
    answer_choices = QuizAnswerChoiceSerializer(many=True)

    class Meta:
        model = QuizAnswer
        fields = '__all__'

    def create(self, validated_data):
        answer_choices_data = validated_data.pop('answer_choices', [])
        quiz_answer = QuizAnswer.objects.create(**validated_data)
        payload = [QuizAnswerChoice(answer_id=quiz_answer, **choice_data) for choice_data in answer_choices_data]
        QuizAnswerChoice.objects.bulk_create(payload)

        return quiz_answer
