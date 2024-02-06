from rest_framework.serializers import ModelSerializer

from blog.models import Advertising


class AdvertisingModelSerializer(ModelSerializer):

    class Meta:
        model = Advertising
        fields = "__all__"

