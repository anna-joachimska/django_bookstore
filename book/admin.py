# Register your models here.
from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['bookstores']
