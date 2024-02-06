from django.contrib import admin

from apps.models import Article, CommentArticle

# Register your models here.

admin.site.register(Article)
admin.site.register(CommentArticle)
