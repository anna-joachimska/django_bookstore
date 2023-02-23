from django.contrib import admin
from .models import Bookstore

@admin.register(Bookstore)
class BookstoreAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['books', "publishing_houses"]

