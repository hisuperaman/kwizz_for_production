from rest_framework import serializers

from .models import Quiz, Question, Choice
from login.models import User


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = "__all__"

class QuestionSerializer(serializers.ModelSerializer):
    choice_set = ChoiceSerializer(many=True)
    class Meta:
        model = Question
        fields = "__all__"

class QuizSerializer(serializers.ModelSerializer):
    question_set = QuestionSerializer(many=True)
    class Meta:
        model = Quiz
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields.pop('user', None)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"