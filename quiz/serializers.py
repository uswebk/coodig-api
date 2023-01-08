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

    def validate(self, attrs):
        # TODO: Validation
        attrs['created_by'] = self.context['request'].user
        return attrs

    def create(self, validate_data):
        quiz = Quiz.objects.create(**validate_data)
        self.create_choices(quiz)
        return quiz

    def create_choices(self, quiz):
        choices = self.context['request'].data['choices']
        for choice in choices:
            choice['quiz_id'] = quiz.id
            quiz_choice_serializer = QuizChoiceSerializer(data=choice)
            quiz_choice_serializer.is_valid(raise_exception=True)
            quiz_choice_serializer.save()


class QuizChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizChoice
        fields = '__all__'

    def validate(self, attrs):
        # TODO: Validation
        return attrs
