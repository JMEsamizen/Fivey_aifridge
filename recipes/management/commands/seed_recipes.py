"""Populate the database with a few sample recipes so the recipes page
and the fridge-based suggestions have something to show.

Usage:
    python manage.py seed_recipes
"""

from django.core.management.base import BaseCommand

from recipes.models import Recipe

# Title -> comma separated ingredients. Keep ingredient names matching common
# fridge products so "Suggestions" can match automatically (e.g. "Eggs").
SAMPLE_RECIPES = [
    ("Vegetable omelette", "Eggs, Cheese, Tomato, Milk"),
    ("Cheese sandwich", "Bread, Cheese, Butter"),
    ("Fruit breakfast bowl", "Apple, Banana, Milk"),
    ("Scrambled eggs", "Eggs, Milk, Butter"),
    ("Tomato cheese salad", "Tomato, Cheese"),
    ("Milk banana smoothie", "Milk, Banana, Juice"),
]


class Command(BaseCommand):
    help = "Seed the database with sample recipes (skips if any already exist)."

    def handle(self, *args, **kwargs):
        if Recipe.objects.exists():
            self.stdout.write(
                self.style.WARNING("Recipes already exist in the database; nothing to seed.")
            )
            return

        for title, ingredients in SAMPLE_RECIPES:
            Recipe.objects.create(title=title, ingredients=ingredients)

        self.stdout.write(
            self.style.SUCCESS(f"Seeded {len(SAMPLE_RECIPES)} sample recipes.")
        )