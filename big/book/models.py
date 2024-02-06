from django.db import models
from django.db.models import Model, CharField, ImageField, FileField, TextField
from rest_framework.fields import IntegerField


# Create your models here.

class Book(Model):
    author = CharField(max_length=255)
    name = CharField(max_length=500, unique=True)
    image = ImageField(null=True, blank=True)
    book = FileField(upload_to='pdfs/', null=True, blank=True)
    description = TextField()

    def __str__(self):
        return self.name


class Vacancy_id(Model):
    id = IntegerField()
    name = CharField(max_length=255)

    class Meta:
        db_table = 'vacancy_id'
