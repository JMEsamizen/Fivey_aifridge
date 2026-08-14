from django.urls import path
from .views import FridgeCreateView, FridgesView

urlpatterns = [
    path('create/', FridgeCreateView.as_view(), name='fridge-create'),
    path('smartfridge/', FridgesView.as_view(), name='smart-fridge'),
]
