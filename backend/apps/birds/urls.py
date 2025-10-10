from django.urls import path
from .views import CaptureBirdView

urlpatterns = [
    path('capture/', CaptureBirdView.as_view(), name='capture-bird'),
]
