from .models import Book
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['uuid', 'name', 'type', 'publishing_house', 'bookstores']
