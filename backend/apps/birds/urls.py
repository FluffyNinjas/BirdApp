from django.urls import path
from .views import BirdListView, CaptureBirdView

urlpatterns = [
    path('list/', BirdListView.as_view(), name='bird-list'),
    path('capture/', CaptureBirdView.as_view(), name='capture-bird'),
]
