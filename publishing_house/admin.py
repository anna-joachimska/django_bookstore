from django.contrib import admin
from .models import PublishingHouse

@admin.register(PublishingHouse)
class PublishingHouseAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']