from django.urls import path
from .views import Mainpageview, FridgesView, MarketsView, RecipiesView, MyHealthView

urlpatterns = [
    path('', Mainpageview.as_view(), name='mainpage'),
    path('/smartfridge', FridgesView.as_view(), name='smart-fridge'),
    path('/markets', MarketsView.as_view(), name='markets'),
    path('/recipies', RecipiesView.as_view(), name='recipies'),
    path('/myhealth', MyHealthView.as_view(), name='my-health'),
]
