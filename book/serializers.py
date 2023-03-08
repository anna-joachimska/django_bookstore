from .models import Book
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class AddBookstoreToBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['bookstores']
