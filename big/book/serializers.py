from rest_framework import serializers

from book.models import Book


class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    # def validate_name(self, value):
    #     if Book.objects.filter(name=value).exists():
    #         raise serializers.ValidationError("Book with this name already exists.")
    #     return value


