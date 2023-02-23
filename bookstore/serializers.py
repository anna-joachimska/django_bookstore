from .models import Bookstore
from rest_framework import serializers

class BookstoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookstore
        fields = ['uuid','name', 'books', 'publishing_houses']