from django.db import models
from login.models import User
from django.utils import timezone

# Create your models here.
class ClientQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    clientquiz_quiz_id = models.IntegerField()
    clientquiz_host_id = models.CharField(max_length=200)

    clientquiz_start_time = models.DateTimeField(default=timezone.localtime)
    clientquiz_end_time = models.DateTimeField()

    clientquiz_time_taken = models.DurationField()

    clientquiz_total_questions = models.IntegerField()
    clientquiz_attempted_questions = models.IntegerField()
    clientquiz_correct_answers = models.IntegerField()

    def __str__(self):
        return f"{self.user.user_username} -> {self.clientquiz_host_id} {self.clientquiz_quiz_id}"


class ClientQuestion(models.Model):
    clientquiz = models.ForeignKey(ClientQuiz, on_delete=models.CASCADE)

    clientquestion_question_id = models.IntegerField()

    def __str__(self):
        return f"{self.clientquestion_question_id}"



class ClientChoice(models.Model):
    clientquestion = models.ForeignKey(ClientQuestion, on_delete=models.CASCADE)

    clientchoice_choice_id = models.IntegerField()
    is_correct_choice = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.clientchoice_choice_id} -> {self.is_correct_choice}"