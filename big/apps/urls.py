from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import ArticleModelView, VacancyModelView, ResumeModelView, GeneratePDFView, \
    LikeArticleView, MyModelView, CommentListAPIView, CommentCreateAPIView, CommentDeleteAPIView, \
    ArticleListView, VacansyListView, ResumeListView, ArticleIdViewModelView, ResumeIdView, \
    VacancyIdView, MyProfileView, MyProfileViewVacansy, MyProfileViewResume

router = DefaultRouter()
router2 = DefaultRouter()
router3 = DefaultRouter()
router4 = DefaultRouter()
# router5 = DefaultRouter()

router.register('article', ArticleModelView, 'article'),
router2.register('vacancy', VacancyModelView, 'vacancy'),
router3.register('resumes', ResumeModelView, 'resumes'),
router4.register('like', LikeArticleView, 'like'),
# router5.register('delete', CommentDeleteAPIView, 'delete'),

urlpatterns = [
    path('article/', include(router.urls)),
    path('article/view_id/<int:pk>/', ArticleIdViewModelView.as_view()),
    path('article-list/', ArticleListView.as_view()),
    path('article/token/<str:token>/', MyProfileView.as_view()),
    # path('article/article_id/<int:article_id>/', MyArticle_idView.as_view()),
    path('vacancy/', include(router2.urls)),
#     path('article/', include(router5.urls)),
    path('vacancy-list/', VacansyListView.as_view()),
    path('vacancy/token/<str:token>/', MyProfileViewVacansy.as_view()),
    path('vacancy/view_id/<int:id>/', VacancyIdView.as_view()),
    path('resume/', include(router3.urls)),
    path('article/', include(router4.urls)),
    path('resume-list/', ResumeListView.as_view()),
    path('resume/token/<str:token>/', MyProfileViewResume.as_view()),
    path('resume/view_id/<int:id>/', ResumeIdView.as_view()),
    path('resume-pdf-generate', GeneratePDFView.as_view()),
    path('coment-list-article', CommentListAPIView.as_view()),
    path('coment-create-article', CommentCreateAPIView.as_view()),
    path('comment/<int:id>/', CommentDeleteAPIView.as_view(), name='comment-delete'),
    path('article/comment/<int:article_id>/', MyModelView.as_view()),

]
