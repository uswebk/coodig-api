from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from quiz.models import Tag, Quiz, QuizChoice


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class QuizSerializer(serializers.ModelSerializer):
    choices = SerializerMethodField()

    class Meta:
        model = Quiz
        fields = '__all__'

    @staticmethod
    def get_choices(obj):
        return QuizChoiceSerializer(QuizChoice.objects.all().filter(quiz_id=obj.id), many=True).data


class QuizChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizChoice
        fields = '__all__'
