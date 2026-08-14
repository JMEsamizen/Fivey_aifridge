from unittest.mock import patch

from django.test import TestCase

from .models import Recipe


class RecipeTests(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(title="Vegetable omelette", ingredients="Eggs, tomato, cheese")

    def test_recipe_list_renders(self):
        response = self.client.get("/recipes/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.recipe.title)

    @patch("recipes.views.calculate_recipe_nutrition")
    def test_nutrition_endpoint_uses_recipe_ingredients(self, nutrition):
        nutrition.return_value = {"calories": 320, "protein": "20g", "carbs": "10g", "fat": "21g"}

        response = self.client.post(
            "/recipes/api/calculate-nutrition/",
            data='{"recipe_id": %d}' % self.recipe.pk,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["calories"], 320)
        nutrition.assert_called_once_with(self.recipe.ingredients)

# Create your tests here.
