from .models import PublishingHouse
from rest_framework import serializers
from book.serializers import BookSerializer


class PublishingHouseSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = PublishingHouse
        fields = '__all__'
