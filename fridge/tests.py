from io import BytesIO
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from .models import Fridge, Product


class FridgeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="safe-password-123")
        self.fridge = Fridge.objects.create(user=self.user)
        self.product = Product.objects.create(fridge=self.fridge, name="Milk")

    def image_file(self):
        buffer = BytesIO()
        Image.new("RGB", (8, 8), "white").save(buffer, format="PNG")
        return SimpleUploadedFile("fridge.png", buffer.getvalue(), content_type="image/png")

    def test_market_inventory_is_preserved_when_ai_detects_no_products(self):
        self.client.force_login(self.user)
        with patch("fridge.views.analyze_media", return_value=[]):
            response = self.client.post("/fridge/smartfridge/", {"file": self.image_file()})

        self.assertRedirects(response, "/fridge/smartfridge/")
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())

    def test_anonymous_user_can_view_upload_screen(self):
        response = self.client.get("/fridge/smartfridge/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Analyze Fridge")

    def test_product_nutrition_fields_default_to_zero(self):
        self.assertEqual(self.product.calories, 0)
        self.assertEqual(self.product.protein, 0)
        self.assertEqual(self.product.carbs, 0)
        self.assertEqual(self.product.fat, 0)

# Create your tests here.
