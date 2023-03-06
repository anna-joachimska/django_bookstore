from .models import PublishingHouse
from rest_framework import serializers


class PublishingHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublishingHouse
        fields = '__all__'
