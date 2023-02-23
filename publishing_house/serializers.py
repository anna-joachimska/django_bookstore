from .models import PublishingHouse
from rest_framework import serializers

class PublishingHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublishingHouse
        fields = ['uuid', 'name', 'books']