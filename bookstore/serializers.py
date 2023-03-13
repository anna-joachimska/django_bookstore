from .models import Bookstore
from rest_framework import serializers
from publishing_house.serializers import PublishingHouseSerializer


class BookstoreSerializer(serializers.ModelSerializer):
    publishing_houses = PublishingHouseSerializer(many=True, read_only=True)

    class Meta:
        model = Bookstore
        fields = '__all__'


class AddPublishingHouseToBookstoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookstore
        fields = ['publishing_houses']
