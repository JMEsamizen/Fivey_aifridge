import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .models import Recipe
from .services import calculate_recipe_nutrition


@ensure_csrf_cookie
def recipes_list(request):
    return render(request, "recipes/recipes.html", {"recipes": Recipe.objects.all()})


@require_POST
def get_nutrition_api(request):
    try:
        payload = json.loads(request.body)
        recipe_id = int(payload["recipe_id"])
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        return JsonResponse({"error": "Invalid recipe request"}, status=400)

    recipe = get_object_or_404(Recipe, pk=recipe_id)
    try:
        nutrition = calculate_recipe_nutrition(recipe.ingredients)
    except Exception:
        return JsonResponse({"error": "Nutrition analysis is temporarily unavailable"}, status=503)

    return JsonResponse(nutrition)
