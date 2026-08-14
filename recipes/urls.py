from django.urls import path
from .views import fridge_recipe_suggestions, recipes_list, get_nutrition_api

urlpatterns = [
    path('', recipes_list, name='recipes'),
    path('suggestions/', fridge_recipe_suggestions, name='fridge-recipe-suggestions'),
    path('api/calculate-nutrition/', get_nutrition_api, name='get_nutrition_api'),
]
