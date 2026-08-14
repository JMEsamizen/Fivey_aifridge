from django.urls import path
from .views import (
    ExpiryNotificationOpenView,
    FridgeCreateView,
    FridgesView,
    ProductDeleteView,
    ProductUpdateView,
)

urlpatterns = [
    path('create/', FridgeCreateView.as_view(), name='fridge-create'),
    path('products/<int:product_id>/edit/', ProductUpdateView.as_view(), name='product-edit'),
    path('products/<int:product_id>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('notifications/<int:notification_id>/open/', ExpiryNotificationOpenView.as_view(), name='notification-open'),
    path('smartfridge/', FridgesView.as_view(), name='smart-fridge'),
]
