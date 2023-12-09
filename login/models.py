from django.db import models

# Create your models here.
class User(models.Model):
    user_uid = models.TextField(unique=True, verbose_name="UID")
    user_username = models.CharField(max_length=200, default=None, null=True, verbose_name="Username")
    user_name = models.CharField(max_length=200, verbose_name="Name")
    user_email = models.CharField(max_length=200, verbose_name="Email")
    user_pfp = models.TextField()

    user_quizzes_hosted = models.IntegerField(default=0)
    user_quizzes_joined = models.IntegerField(default=0)

    def __str__(self):
        return self.user_username