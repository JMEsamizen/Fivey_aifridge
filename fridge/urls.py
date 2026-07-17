from django.urls import path
from .views import FridgeCreateView
urlpatterns = [
    path('create/', FridgeCreateView.as_view(), name='fridge-create'),
]