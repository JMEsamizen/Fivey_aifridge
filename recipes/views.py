import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .models import Recipe
from .services import calculate_recipe_nutrition
from fridge.models import Product


@ensure_csrf_cookie
def recipes_list(request):
    return render(request, "recipes/recipes.html", {"recipes": Recipe.objects.all()})


@login_required
def fridge_recipe_suggestions(request):
    focus_product = request.GET.get("product", "").strip()
    fridge_products = Product.objects.filter(fridge__user=request.user)
    product_names = [product.name for product in fridge_products]

    suggestions = []
    for recipe in Recipe.objects.all():
        ingredients = recipe.ingredients.casefold()
        matched_products = [
            product_name
            for product_name in product_names
            if product_name.casefold() in ingredients
        ]
        is_focus_match = focus_product.casefold() in ingredients if focus_product else False

        if matched_products and (not focus_product or is_focus_match):
            suggestions.append({
                "recipe": recipe,
                "matched_products": matched_products,
                "is_focus_match": is_focus_match,
            })

    suggestions.sort(
        key=lambda suggestion: (
            suggestion["is_focus_match"],
            len(suggestion["matched_products"]),
        ),
        reverse=True,
    )
    return render(
        request,
        "recipes/fridge_suggestions.html",
        {
            "focus_product": focus_product,
            "suggestions": suggestions,
        },
    )


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
