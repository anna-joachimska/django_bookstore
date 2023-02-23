from django.urls import path
from .views import BooksView, BookDetail

urlpatterns = [
    path('', BooksView.as_view()),
    path('<str:pk>', BookDetail.as_view()),
]