from django.urls import path
from .views import BooksView, BookDetail, AddOrRemoveBookstoreFromBook

urlpatterns = [
    path('', BooksView.as_view()),
    path('<str:pk>', BookDetail.as_view()),
    path('add-or-remove-bookstore/<str:pk>', AddOrRemoveBookstoreFromBook.as_view()),

]
