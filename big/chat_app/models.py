from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

from google_login.models import User


class Room(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    current_users = models.ManyToManyField(User, related_name="current_rooms", blank=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username


ad0387917 = models.ForeignKey