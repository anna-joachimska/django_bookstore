from django.urls import path
from .views import BookstoresView, BookstoreDetail, BookstoreBooks, BookstorePublishingHouses

urlpatterns = [
    path('', BookstoresView.as_view()),
    path('<str:pk>', BookstoreDetail.as_view()),
    path('add-books/<str:pk>', BookstoreBooks.as_view()),
    path('add-publishing-houses/<str:pk>', BookstorePublishingHouses.as_view()),
]