from rest_framework.routers import DefaultRouter
from django.urls import path, include

from book.views import BookUploadView, DownloadPDFView

router = DefaultRouter()

router.register('book', BookUploadView, 'book')

urlpatterns = [
    path('', include(router.urls)),
    path('api/books/<int:pk>/download/', DownloadPDFView.as_view(), name='download-pdf'),

]