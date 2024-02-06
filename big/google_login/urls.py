from django.urls import path

from google_login.views import GoogleSocialAuthView

urlpatterns = [
    path('google/', GoogleSocialAuthView.as_view()),
]
