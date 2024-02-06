from django.urls import path

from blog.views import AdvertisingModelViewSet

urlpatterns = [
    path('blog/', AdvertisingModelViewSet.as_view, name='blogs')
]
