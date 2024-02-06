from django.db import models
from django.db.models import Model, CharField, TextField, CASCADE


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'


class Direct_video(Model):
    title = CharField(max_length=255, unique=True)
    image = models.FileField(upload_to='image/', null=True, blank=True)
    description = TextField()
    added_time = models.DateTimeField(auto_now_add=True)
    link = models.URLField(max_length=300, blank=True)
    category = models.ForeignKey(Category, on_delete=CASCADE, to_field='name')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'direct_video'
