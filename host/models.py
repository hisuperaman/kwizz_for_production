from django.db import models
from django.utils import timezone

# Create your models here.
class Quiz(models.Model):
    quiz_id = models.IntegerField()
    quiz_host_id = models.TextField()

    quiz_title = models.TextField()
    quiz_timer_minutes = models.IntegerField()

    quiz_publish_date = models.DateTimeField(default=timezone.localtime)
    quiz_start_date = models.DateTimeField(null=True ,default=None)

    quiz_is_held = models.BooleanField(default=False)
    quiz_visible = models.BooleanField(default=True)

    quiz_no_of_users = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.quiz_id>1030:
            next_quiz_id = self.get_next_available_quiz_id()
            self.quiz_id = next_quiz_id

        super().save(*args, **kwargs)

    def get_next_available_quiz_id(self):
        filtered_data = Quiz.objects.filter(quiz_host_id=self.quiz_host_id)
        existing_quiz_ids = filtered_data.values_list("quiz_id", flat=True)
        total_quiz_ids = range(1000, 1031)
        available_quiz_ids = set(total_quiz_ids) - set(existing_quiz_ids)
        if available_quiz_ids:
            return min(available_quiz_ids)
        else:
            raise ValueError("Quiz limit reached.")


    def __str__(self):
        return f"{self.quiz_host_id}{self.quiz_id} -> {self.quiz_title}"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    question_id = models.IntegerField()
    question_text = models.TextField()

    def __str__(self):
        return f"{self.question_id} -> {self.question_text}"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    choice_id = models.IntegerField()
    choice_text = models.TextField()
    is_correct_choice = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.choice_id} -> {self.choice_text}"