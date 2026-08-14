from django.urls import path
from .views import recipes_list, get_nutrition_api 

urlpatterns = [
    path('', recipes_list, name='recipes'),
    path('api/calculate-nutrition/', get_nutrition_api, name='get_nutrition_api'),
]
