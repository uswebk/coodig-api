from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from quiz.models import Tag, Quiz, QuizChoice


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class QuizSerializer(serializers.ModelSerializer):
    question = serializers.CharField()
    is_published = serializers.BooleanField()
    is_deleted = serializers.BooleanField()
    choices = SerializerMethodField()

    class Meta:
        model = Quiz
        fields = '__all__'

    @staticmethod
    def get_choices(obj):
        return QuizChoiceSerializer(QuizChoice.objects.all().filter(quiz_id=obj.id), many=True).data


class QuizChoiceSerializer(serializers.ModelSerializer):
    sentence = serializers.CharField()
    is_answer = serializers.BooleanField()
    sort = serializers.IntegerField()

    class Meta:
        model = QuizChoice
        fields = '__all__'
