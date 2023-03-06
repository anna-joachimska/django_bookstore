from django.urls import path
from .views import PublishingHousesView, PublishingHouseDetail

urlpatterns = [
    path('', PublishingHousesView.as_view()),
    path('<str:pk>', PublishingHouseDetail.as_view()),
]
