from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from direct_video.models import Category, Direct_video


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

    # def validate_name(self, value):
    #     if Category.objects.filter(name=value).exists():
    #         raise serializers.ValidationError("Category with this name already exists.")
    #     return value


class Direct_videoSerializer(serializers.ModelSerializer):
    category_name = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='name',
        source='category',
    )

    class Meta:
        model = Direct_video
        fields = ['title', 'image', 'description', 'added_time', 'link', 'category_name']

    # def validate_name(self, value):
    #     if Category.objects.filter(title=value).exists():
    #         raise serializers.ValidationError("Video with this title already exists.")
    #     return value
