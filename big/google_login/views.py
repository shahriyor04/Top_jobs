from django.shortcuts import render
from drf_yasg.openapi import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from google_login.serializers import GoogleSocialAuthSerializer


class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)