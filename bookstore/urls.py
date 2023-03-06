from django.urls import path
from .views import BookstoresView, BookstoreDetail, AddOrDeletePublishingHouseFromBookstore

urlpatterns = [
    path('', BookstoresView.as_view()),
    path('<str:pk>', BookstoreDetail.as_view()),
    path('add-or-remove-publishing-house/<str:pk>', AddOrDeletePublishingHouseFromBookstore.as_view()),
]
