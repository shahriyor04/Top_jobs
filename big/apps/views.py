import os
import smtplib
import ssl
from datetime import datetime
from email.message import EmailMessage

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.models import Article, Vacancy, Resumes, CommentArticle, LikeArticle
from apps.permissions import PostPermission
from apps.serializers import ArticleSerializer, VacancySerializer, ResumeSerializer, CommentSerializer, \
    LikeArticleSerializer, ArticleViewId, ArticleListSerializer, VacancyListSerializer
from apps.service import add_profile_section, add_education_section, add_work_experience_section, add_skills
from singin.models import MyProfile

"""----------------------------Article------------------------------------"""


class ArticleModelView(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    parser_classes = (MultiPartParser,)
    permissions = (IsAuthenticated, PostPermission)
    http_method_names = ('post', 'patch', 'delete')


class ArticleIdViewModelView(RetrieveModelMixin, GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleViewId
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class LikeArticleView(ModelViewSet):
    queryset = LikeArticle.objects.all()
    serializer_class = LikeArticleSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ('post',)


class ArticleListView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['title', ]


class MyProfileView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def get_object(self):
        token = self.kwargs['token']
        queryset = self.filter_queryset(MyProfile.objects.all())

        try:
            obj = queryset.get(token=token)
            return obj
        except MyProfile.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance is not None:
            user = instance.user
            user_articles = Article.objects.filter(user=user)

            if user_articles.exists():
                serialized_articles = []
                for article in user_articles:
                    article_data = ({
                        'id': article.id,
                        'title': article.title,
                        'description': article.description,
                        # 'image': article.image.url if article.image.url else None
                    })
                    if article.image:
                        article_data['image'] = request.build_absolute_uri(article.image.url)
                    else:
                        article_data['image'] = None

                    serialized_articles.append(article_data)

                user_data = {
                    # 'username': user.username,
                    # 'email': user.email,
                    ''
                    'Articles_access': True,
                    'articles': serialized_articles,
                }
                return Response({'exists': True, 'user_data': user_data}, status=status.HTTP_200_OK)
            else:
                user_data = {
                    'username': user.username,
                    'email': user.email,
                    'Articles_access': False,
                    'articles': [],
                }
                return Response({'exists': True, 'user_data': user_data}, status=status.HTTP_200_OK)
        else:
            return Response({'exists': False}, status=status.HTTP_404_NOT_FOUND)


class MyModelView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, article_id):
        comments = CommentArticle.objects.filter(article_id=article_id)
        serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentListAPIView(ListAPIView):
    queryset = CommentArticle.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get']


class CommentCreateAPIView(CreateAPIView):
    queryset = CommentArticle.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']


class CommentDeleteAPIView(DestroyAPIView):
    queryset = CommentArticle.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, PostPermission]
    http_method_names = ['delete']


"""----------------------------Vacansy------------------------------------"""


class VacancyModelView(ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permissions = (IsAuthenticated, PostPermission)
    parser_classes = (MultiPartParser,)

    http_method_names = ('post', 'patch', 'delete')

    emails = ['mirazizmirpolatov9@gmail.com', 'shahriyorboronov04@gmail.com']

    def perform_create(self, serializer):
        job = serializer.validated_data['job']
        link = f"https://example.com/{job.replace(' ', '-')}"
        serializer.save(link=link)

    def send_email_to_users(self, request):
        if request.method == 'post':
            job = request.data.get('job')
            if job:
                self.send_message_to_email(job)
                return Response({"message": f"Email sent successfully for {job}!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Job is required in the request data."}, status=status.HTTP_400_BAD_REQUEST)

    def send_message_to_email(self, job):
        email_sender = 'boronovshahriyor2004@gmail.com'
        email_password = 'sqip huze ceri llpz'
        # email_receivers = [self.emails for email in self.emails]
        email_receivers = self.emails
        subject = job
        body = f'Bizda yangi vakansiya : {job} '
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receivers
        em['Subject'] = subject
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receivers, em.as_string())


class VacansyListView(ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['job', 'company', 'address']


class MyProfileViewVacansy(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = VacancySerializer
    queryset = Vacancy.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self):
        token = self.kwargs['token']
        queryset = self.filter_queryset(MyProfile.objects.all())

        try:
            obj = queryset.get(token=token)
            return obj
        except MyProfile.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance is not None:
            user = instance.user
            user_vacancy = Vacancy.objects.filter(user=user)

            if user_vacancy.exists():
                serialized_vacancy = []
                for vacancy in user_vacancy:
                    serialized_vacancy.append({
                        'id': vacancy.id,
                        'company': vacancy.company,
                        'job': vacancy.job,
                        'experience': vacancy.experience,
                        'working_time': vacancy.job,
                        'address': vacancy.address,
                        'phone_number': vacancy.phone_number,
                        'tg_link': vacancy.tg_link,
                        'salary': vacancy.salary,
                        'requirements': vacancy.requirements,
                        'conditions': vacancy.conditions,
                    })

                user_data = {
                    # 'username': user.username,
                    # 'email': user.email,
                    'Vacancy_access': True,
                    'vacancy': serialized_vacancy,

                }
                return Response({'exists': True, 'user_data': user_data}, status=status.HTTP_200_OK)
            else:
                user_data = {
                    'username': user.username,
                    'email': user.email,
                    'Vacancy_access': False,
                    'vacancy': [],  # No articles for this user
                }
                return Response({'exists': True, 'user_data': user_data}, status=status.HTTP_200_OK)
        else:
            return Response({'exists': False}, status=status.HTTP_404_NOT_FOUND)


class VacancyIdView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        try:
            resume = Vacancy.objects.get(id=id)
            serializer = VacancySerializer(resume)
            return Response(serializer.data)
        except Vacancy.DoesNotExist:
            return Response({"errors": "Vacancy not found"}, status=404)


"""----------------------------Resume------------------------------------"""


class ResumeListView(ListAPIView):
    queryset = Resumes.objects.all()
    serializer_class = ResumeSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['level', 'job']


class MyProfileViewResume(GenericAPIView):
    serializer_class = ResumeSerializer
    queryset = Resumes.objects.all()

    def get_object(self):
        token = self.kwargs['token']
        queryset = self.filter_queryset(MyProfile.objects.all())

        try:
            obj = queryset.get(token=token)
            return obj
        except MyProfile.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance is not None:
            user = instance.user
            user_resume = Resumes.objects.filter(user=user)

            if user_resume.exists():
                serialized_resumes = []
                for resume in user_resume:
                    serialized_resumes.append({
                        'id': resume.id,
                        'last_name': resume.last_name,
                        'date_of_birth': resume.date_of_birth,
                        'job': resume.job,
                        'level': resume.level,
                        'address': resume.address,
                        'phone_number': resume.phone_number,
                        'github': resume.github,
                        'working_time': resume.working_time,
                        'salary': resume.salary,
                        'about_me': resume.about_me,
                        'skills': resume.skills,
                        'school': resume.school,
                        'education_direction': resume.education_direction,
                        'education_date': resume.education_date,
                        'company': resume.company,
                        'work_experience_direction': resume.work_experience_direction,
                        'work_experience_date': resume.work_experience_date,
                    })

                user_data = {
                    # 'username': user.username,
                    # 'email': user.email,
                    'resume': serialized_resumes,
                }
                return Response({'exists': True, 'user_data': user_data}, status=status.HTTP_200_OK)
            else:
                user_data = {
                    'username': user.username,
                    'email': user.email,
                    'resume': [],  # No articles for this user
                }
                return Response({'exists': True, 'user_data': user_data}, status=status.HTTP_200_OK)
        else:
            return Response({'exists': False}, status=status.HTTP_404_NOT_FOUND)


class ResumeModelView(ModelViewSet):
    queryset = Resumes.objects.all()
    serializer_class = ResumeSerializer
    permissions = (IsAuthenticated, PostPermission)
    parser_classes = (MultiPartParser,)

    http_method_names = ('post', 'patch', 'delete')


class ResumeIdView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        try:
            resume = Resumes.objects.get(id=id)
            serializer = ResumeSerializer(resume)
            return Response(serializer.data)
        except Resumes.DoesNotExist:
            return Response({"errors": "Resume not found"}, status=404)


class GeneratePDFView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Resumes.objects.filter(user_id=self.request.user.id)
        instance = queryset.first()

        if instance:
            pdf_path = os.path.join("resume.pdf")
            self.create_pdf(pdf_path, instance)
            try:
                with open(pdf_path, 'rb') as pdf_file:
                    response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
                    os.remove(pdf_path)
                    return response
            except FileNotFoundError:
                return Response({'detail': 'File Not Found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': 'No resumes available.'}, status=status.HTTP_404_NOT_FOUND)

    def create_pdf(self, pdf_path, resume_instance):
        c = canvas.Canvas(pdf_path, pagesize=A4)
        w, h = A4

        # Set font styles
        c.setFont("Helvetica-Bold", 24)
        c.setFillColorRGB(0, 51, 102)  # Dark blue color

        # Header Section
        c.drawString(50, h - 50, resume_instance.last_name)
        c.setFont("Helvetica", 18)
        c.setFillColorRGB(0, 0, 0)  # Black color
        yosh = str(resume_instance.date_of_birth).split('-')[0]
        today = str(datetime.now()).split('-')[0]
        brith_day = str(resume_instance.date_of_birth).split(' ')[0]
        c.drawString(50, h - 80, f"Date of Birth: {brith_day}  age {int(today) - int(yosh)}")

        # Line separator
        c.line(50, h - 100, w - 50, h - 100)

        # Profile Section
        add_profile_section(c, resume_instance)

        # Education Section
        add_education_section(c, resume_instance)

        # # Work Experience Section
        add_work_experience_section(c, resume_instance)
        add_skills(c, resume_instance)

        c.showPage()
        c.save()
