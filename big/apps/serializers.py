from rest_framework.exceptions import ValidationError
from rest_framework.fields import HiddenField, CurrentUserDefault, SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from apps.models import Article, Vacancy, Resumes, CommentArticle, LikeArticle, MyArticle, MyVacancy, MyResume


class ArticleSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    username = SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'username', 'user', 'image', 'title', 'description', 'created_at')

    def get_username(self, obj):
        return obj.user.username


class ArticleListSerializer(ModelSerializer):
    username = SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'username', 'image', 'title', 'description', 'is_activ', 'created_at')

    def get_username(self, obj):
        return obj.user.username


class ArticleViewId(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    username = SerializerMethodField()
    total_likes = SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'username', 'user', 'image', 'title', 'description', 'created_at', 'view', 'total_likes')

    def get_username(self, obj):
        return obj.user.username

    def get_total_likes(self, obj):
        return LikeArticle.objects.filter(article=obj).count()


class VacancyListSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Vacancy
        fields = 'id', 'user', 'company', 'job', 'experience', 'working_time', 'created_at'


class VacancySerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Vacancy
        fields = 'id', 'user', 'company', 'job', 'experience', 'working_time', 'address', 'phone_number', 'tg_link', 'salary', 'requirements', 'conditions', 'created_at'


class ResumeSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    username = SerializerMethodField()

    class Meta:
        model = Resumes
        fields = (
            'id', 'username',
            'last_name', 'image', 'date_of_birth', 'job', 'level', 'address', 'phone_number',
            'github', 'working_time', 'salary', 'about_me',
            'skills', 'school', 'education_direction', 'education_date', 'company',
            'work_experience_direction',
            'work_experience_date', 'created_at', 'user')

    def get_username(self, obj):
        return obj.user.username


class CommentSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    username = SerializerMethodField()

    class Meta:
        model = CommentArticle
        fields = 'id', 'username', 'user', 'text', 'article', 'posted_on'

    def get_username(self, obj):
        return obj.user.username


class ResumePdfSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Resumes
        fields = ('user',)


class LikeArticleSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = LikeArticle
        fields = ('user', 'article')

    def create(self, validated_data):
        user = validated_data['user']
        article = validated_data['article']
        like = LikeArticle.objects.filter(user=user, article=article).first()
        if like:
            like.delete()
            return {'message': "unlike article"}
        else:
            like_instance = LikeArticle.objects.create(user=user, article=article)
            return like_instance

    def to_representation(self, instance):
        if isinstance(instance, dict):
            return instance

        return super().to_representation(instance)


class MyArticleSerializer(ModelSerializer):
    class Meta:
        model = MyArticle
        fields = ('token',)


class MyVacancySerializer(ModelSerializer):
    class Meta:
        model = MyVacancy
        fields = ('token',)


class MyResumeSerializer(ModelSerializer):
    class Meta:
        model = MyResume
        fields = ('token',)
