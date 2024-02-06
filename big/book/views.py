from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from book.models import Book
# from book.permissions import IsSuperUser
from book.serializers import BookSerializers


# Create your views here.


class BookUploadView(ModelViewSet):
    serializer_class = BookSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser,)
    queryset = Book.objects.all()
    http_method_names = ('get',)

    def post(self, request, *args, **kwargs):
        if request.FILES and 'upload' in request.FILES:
            upload = request.FILES['upload']
            fss = FileSystemStorage()
            file = fss.save(upload.name, upload)
            file_url = fss.url(file)
            return Response({'file_url': file_url}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DownloadPDFView(APIView):
    def get(self, request, pk):
        book_pdfs = get_object_or_404(Book, pk=pk)
        pdf_path = book_pdfs.book.path

        with open(pdf_path, 'rb') as pdf_file:
            pdf_data = pdf_file.read()

        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{book_pdfs.name}.pdf"'

        return response
