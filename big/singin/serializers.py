from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.fields import CharField, EmailField
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError

from google_login.models import User
from singin.models import Verification, MyProfile


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class My_account(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class My_Profile(ModelSerializer):
    class Meta:
        model = MyProfile
        fields = ('token',)


class UserCreateModelSerializer(ModelSerializer):
    confirm_password = CharField(max_length=255, read_only=True)

    def validate(self, data: dict):
        data['password'] = make_password(data['password'])
        return data

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'email')


class VerificationSerializer(ModelSerializer):
    class Meta:
        model = Verification
        fields = ('email', 'verification_code')


class EmailSerializer(UserCreateModelSerializer):
    class Meta:
        model = User
        fields = ("email",)


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        min_length=1,
    )
    verification_code = serializers.CharField(max_length=6)
    email = serializers.EmailField()

    class Meta:
        field = '__all__'
