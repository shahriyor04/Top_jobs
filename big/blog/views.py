from rest_framework.viewsets import ModelViewSet

from blog.models import Advertising
from blog.serializers import AdvertisingModelSerializer


class AdvertisingModelViewSet(ModelViewSet):
    queryset = Advertising.objects.all()
    serializer_class = AdvertisingModelSerializer

