from django.db import models
from django.db.models import Model


class Advertising(Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)
    media = models.FileField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
