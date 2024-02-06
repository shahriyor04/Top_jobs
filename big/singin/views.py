import random
import smtplib
import ssl
from email.message import EmailMessage

from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from google_login.models import User
from .models import Verification, MyProfile
from .serializers import UserCreateModelSerializer, VerificationSerializer, ResetPasswordSerializer, EmailSerializer, \
    My_account, My_Profile, UserSerializer
from .tasks import send_email_async


class UsersCreateAPIView(GenericAPIView):
    serializer_class = UserCreateModelSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        def send_email_async(email, random_code):
            email_sender = 'boronovshahriyor2004@gmail.com'  # noqa
            email_password = 'sqip huze ceri llpz'  # noqa
            subject = "salom"
            body = f"Tasdiqlash kodi: {random_code}"  # noqa

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email
            em['Subject'] = subject
            em.set_content(body)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email, em.as_string())

        email = request.data.get('email')
        if email:
            random_code = generate_random_code()
            Verification.objects.create(user=user, email=email, verification_code=random_code)
            send_email_async(email=email, random_code=random_code)
            return Response({"message": f"Email sent successfully for {email}!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Email is required in the request data."}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()  # Set your queryset here
    serializer_class = My_account  # Use your UserSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyProfileView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = My_Profile
    queryset = MyProfile.objects.all()

    def get_object(self):
        token = self.kwargs['token']
        queryset = self.filter_queryset(self.get_queryset())

        try:
            obj = queryset.get(token=token)
            return obj
        except MyProfile.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            if instance is not None:
                user_data = {
                    'username': instance.user.username,
                    'email': instance.user.email,
                }
                return Response({'exists': True, 'user_data': user_data}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)



class Login(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not (email and password):
            raise AuthenticationFailed('email va parol kiritishingiz kerak!')

        user = authenticate(email=email, password=password)

        if user is None:
            raise AuthenticationFailed('Foydalanuvchi topilmadi yoki parol noto\'g\'ri!')

        tk = RefreshToken.for_user(user)
        token = {
            'refresh_token': str(tk),
            'access_token': str(tk.access_token)
        }
        MyProfile.objects.create(user=user, token=token['access_token'])
        return Response(token, status=status.HTTP_200_OK)


class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerificationSerializer

    def post(self, request):
        email = request.data.get('email')
        verification_code = request.data.get('verification_code')

        if not (email and verification_code):
            raise AuthenticationFailed('email va tasdiqlash kodi kiritishingiz kerak!')

        try:
            verification = Verification.objects.get(email=email, verification_code=verification_code)
            user = verification.user
        except (User.DoesNotExist, Verification.DoesNotExist):
            raise AuthenticationFailed('Foydalanuvchi topilmadi yoki tasdiqlash kodi noto\'g\'ri!')
        tk = RefreshToken.for_user(user)
        token = {
            'refresh_token': str(tk),
            'access_token': str(tk.access_token)
        }
        MyProfile.objects.create(user=user, token=token['access_token'])
        return Response(token, status=status.HTTP_200_OK)


class PasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmailSerializer

    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
            random_code = generate_random_code()
            Verification.objects.create(user=user, verification_code=random_code)
            send_email_async(email=email, random_code=random_code)

            return Response({"message": f"Email sent successfully for {email}"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle other specific exceptions that might occur during the process
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def generate_random_code():
    return random.randint(100000, 999999)


class ResetPasswordAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Access validated data from serializer
        password = serializer.validated_data.get('password')
        verification_code = serializer.validated_data.get('verification_code')
        email = serializer.validated_data.get('email')

        try:
            user = User.objects.get(email=email)
            verification_obj = Verification.objects.get(user=user, verification_code=verification_code)

            # Check if the verification code matches
            if not verification_obj.verification_code == verification_code:
                user.set_password(password)
                user.save()

                # Invalidate or delete the verification code here if needed

                return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
            else:
                # Invalid verification code for this user
                return Response({"error": "Invalid verification code for this user"},
                                status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Verification.DoesNotExist:
            # Invalid verification code for any user
            return Response({"error": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
