from django.db import models

# Create your models here.
class User(models.Model):
    user_uid = models.TextField(unique=True)
    user_username = models.TextField(default=None, null=True)
    user_name = models.TextField()
    user_email = models.TextField()
    user_pfp = models.TextField()

    user_quizzes_hosted = models.IntegerField(default=0)
    user_quizzes_joined = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user_uid} -> {self.user_name}"