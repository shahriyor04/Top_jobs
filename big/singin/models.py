from django.db import models
from django.db.models import CASCADE

from google_login.models import User as YourUserModel, User


class Verification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    verification_code = models.IntegerField()

    def __str__(self):
        return self.user.username


class MyProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

    def __str__(self):
        return self.token
