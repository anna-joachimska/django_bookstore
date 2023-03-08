from .models import Bookstore
from rest_framework import serializers


class BookstoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookstore
        fields = '__all__'


class AddPublishingHouseToBookstoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookstore
        fields = 'publishing_houses'
