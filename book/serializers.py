from .models import Book
from rest_framework import serializers
from bookstore.serializers import BookstoreSerializer


class BookSerializer(serializers.ModelSerializer):
    bookstores = BookstoreSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'


class AddBookstoreToBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['bookstores']
