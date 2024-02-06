from django.urls import path, include
from rest_framework.routers import DefaultRouter

from direct_video.views import DirectUploadView

router = DefaultRouter()
router.register('direct_video', DirectUploadView, 'direct_video')
urlpatterns = [
    path('', include(router.urls))
    # path('categories/', CategoryView.as_view(), name='category-list-create'),
    # path('direct_video/', DirectUploadView.as_view, name='video-list-create'),
    # path('api/video/<int:pk>/get', MyDirectView.as_view(), name='video_get')
]
