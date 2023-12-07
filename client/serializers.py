from rest_framework import serializers
from .models import ClientQuiz, ClientQuestion, ClientChoice
from login.models import User

class ClientChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientChoice
        fields = "__all__"

class ClientQuestionSerializer(serializers.ModelSerializer):
    clientchoice_set = ClientChoiceSerializer(many=True)
    class Meta:
        model = ClientQuestion
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ClientQuizSerializer(serializers.ModelSerializer):
    clientquestion_set = ClientQuestionSerializer(many=True)
    user = UserSerializer()
    class Meta:
        model = ClientQuiz
        fields = "__all__"