from django.urls import path
from .views import BooksView, BookDetail, AddOrDeleteBookstoreFromBook

urlpatterns = [
    path('', BooksView.as_view()),
    path('<str:pk>', BookDetail.as_view()),
    path('add-or-delete-bookstore/<str:pk>', AddOrDeleteBookstoreFromBook.as_view()),

]
