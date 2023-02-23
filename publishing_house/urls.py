from django.urls import path
from .views import PublishingHousesView, PublishingHouseDetail, PublishingHouseBooks

urlpatterns = [
    path('', PublishingHousesView.as_view()),
    path('<str:pk>', PublishingHouseDetail.as_view()),
    path('add-books/<str:pk>', PublishingHouseBooks.as_view()),
]