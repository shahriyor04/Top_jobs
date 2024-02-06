from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenRefreshView)


from singin.views import UsersCreateAPIView, LoginView, PasswordReset, ResetPasswordAPIView, UserDetailView, \
    MyProfileView, Login

router = DefaultRouter()

urlpatterns = (
    # path('register/', UserCreateAPIView.as_view({'post': 'create'}), name='register'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('login', Login.as_view(), name='login'),
    path('register/', UsersCreateAPIView.as_view(), name='register'),
    # path('my-profile/<int:pk>', UserDetailView.as_view(), name='user-profile'),
    path('my-profile/<str:token>/', MyProfileView.as_view(), name='user-profile'),
    path('login/6_number/', LoginView.as_view(), name='login_6_number'),
    path('request-password-email/', PasswordReset.as_view(), name="request-password-email"),
    # path('password-reset/', ResetPasswordAPI.as_view(), name="request-password-reset"),
    path('request-password/', ResetPasswordAPIView.as_view(), name="request-password",),

    path('', include(router.urls)),
)
