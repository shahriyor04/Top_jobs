from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView

CALLBACK_URL_YOU_SET_ON_GOOGLE = "https://example.com/callback"


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = CALLBACK_URL_YOU_SET_ON_GOOGLE
    client_class = OAuth2Client


class UserRedirectView(LoginRequiredMixin, RedirectView):


    permanent = False

    def get_redirect_url(self):
        return "redirect-url"