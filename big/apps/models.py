from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE, DateTimeField

from Tob_jobs2 import settings


class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, CASCADE)
    image = models.ImageField(upload_to='image/', null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    comment = models.ForeignKey('CommentArticle', CASCADE, related_name='article_comment', null=True, blank=True)
    is_activ = models.BooleanField(default=False, null=True, blank=True)
    view = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_number_of_views(self):
        self.view += 1
        return 0

    def __str__(self):
        return self.title
    #


class MyArticle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)


class LikeArticle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, CASCADE)
    article = models.ForeignKey(Article, on_delete=CASCADE, related_name='article')


class CommentArticle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, CASCADE)
    article = models.ForeignKey(Article, CASCADE)
    text = models.TextField()
    posted_on = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Vacancy(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, CASCADE)
    company = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    working_time = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    tg_link = models.URLField(null=True, blank=True)
    salary = models.CharField(max_length=100, blank=True, null=True)
    requirements = models.CharField(max_length=500, null=True, blank=True)
    conditions = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField()


class MyVacancy(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)


class Resumes(models.Model):
    Choice = (
        ('intern', 'Intern'),
        ('junior', 'Junior'),
        ('middle', 'Middle'),
        ('senior', 'Senior'),
        ('team lead', 'Team Load'),
    )

    Employment = (('part time', 'Part time'),
                  ('full time', 'Full time'),
                  ('remote working time', 'Remote working time'))
    last_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    date_of_birth = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name='resume')
    job = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=Choice)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
    github = models.URLField()
    working_time = models.CharField(max_length=50, choices=Employment)
    salary = models.CharField(max_length=50)
    about_me = models.CharField(max_length=255)
    skills = models.CharField(max_length=255)
    school = models.CharField(max_length=100, blank=True, null=True)
    education_direction = models.CharField(max_length=255, null=True, blank=True)
    education_date = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    work_experience_direction = models.CharField(max_length=255, null=True, blank=True)
    work_experience_date = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class MyResume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
