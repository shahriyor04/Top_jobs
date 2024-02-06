from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, serializers
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from direct_video.filters import DirectVideoFilter
from direct_video.models import Direct_video, Category
# from direct_video.permissions import IsSuperUser
from direct_video.serializers import Direct_videoSerializer, CategorySerializer


class DirectUploadView(ModelViewSet):
    serializer_class = Direct_videoSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser,)
    queryset = Direct_video.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = DirectVideoFilter
    http_method_names = ('get',)


# class MyDirectView(APIView):
#     def get_object(self, pk):
#         try:
#             return Direct_video.objects.get(pk=pk)
#         except:
#             raise serializers.ValidationError(f'Malumotlar bazasida {pk} video mavjud emas')
#
#     def get(self, request, pk, *args, **kwargs):
#         instance = self.get_object(pk)
#         serializer = Direct_videoSerializer(instance)
#         return Response(serializer.data, status.HTTP_200_OK)


class CategoryView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    http_method_names = ('get',)
