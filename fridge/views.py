from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from django.db import transaction
from datetime import datetime
from PIL import Image, UnidentifiedImageError

from .models import Fridge, Product
from .additional_func import get_product_shape
from user.ai_utils import analyze_media

from django.contrib import messages

class FridgeCreateView(View):

    def post(self, request):

        if not request.user.is_authenticated:
            return redirect("login")

        name = request.POST.get("name", "").strip()
        quantity = request.POST.get("quantity", "1")
        expire_date = request.POST.get("expire_date")

        if not name:
            messages.error(request, "Product name is required")
            return redirect("smart-fridge")
        
        if len(name) > 100:
            messages.error(request, "Product name is too long")
            return redirect("smart-fridge")

        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            messages.error(request, "Quantity must be a number")
            return redirect("smart-fridge")

        if not 1 <= quantity <= 10000:
            messages.error(request, "Quantity must be between 1 and 10,000")
            return redirect("smart-fridge")

        parsed_expire_date = None

        if expire_date:
            try:
                parsed_expire_date = datetime.strptime(
                    expire_date,
                    "%Y-%m-%d"
                ).date()
            except ValueError:
                messages.error(request, "Invalid expiration date")
                return redirect("smart-fridge")

            if parsed_expire_date < timezone.localdate():
                messages.error(request, "Expiration date cannot be in the past")
                return redirect("smart-fridge")

        fridge, created = Fridge.objects.get_or_create(
            user=request.user
        )

        Product.objects.create(
            fridge=fridge,
            name=name,
            quantity=quantity,
            expire_date=parsed_expire_date,
            model_2d=get_product_shape(name)
        )

        messages.success(request, "Product added to your fridge")
        return redirect("smart-fridge")


class FridgesView(View):

    def get(self, request):

        if not request.user.is_authenticated:
            return render(
                request,
                "fridge/smartfridges.html",
                {
                    "new_user": True
                }
            )

        fridge, created = Fridge.objects.get_or_create(
            user=request.user
        )

        products = list(
            fridge.products.all()
        )

        shelves = [
            products[i:i + 5]
            for i in range(0, len(products), 5)
        ]

        return render(
            request,
            "fridge/smartfridges.html",
            {
                "new_user": not products,
                "products": products,
                "shelves": shelves,
                "fridge": fridge
            }
        )

    def post(self, request):

        if not request.user.is_authenticated:
            return redirect("login")

        file = request.FILES.get("file")

        if not file:
           messages.error(request, "File not selected")
           return redirect("smart-fridge")
        allowed_types = [
            "image/jpeg",
            "image/png",
            "image/webp"
        ]

        if file.content_type not in allowed_types:
            messages.error( request, "Only JPG, PNG and WEBP images are allowed")
            return redirect("smart-fridge")

        if file.size > 10 * 1024 * 1024:
            messages.error(request, "Image size must be less than 10 MB")
            return redirect("smart-fridge")

        try:
            Image.open(file).verify()
            file.seek(0)
        except (UnidentifiedImageError, OSError):
            messages.error(request, "The uploaded file is not a valid image")
            return redirect("smart-fridge")

        products = analyze_media(file)

        if not isinstance(products, list):
            messages.error(request, "Could not analyze the image")
            return redirect("smart-fridge")

        fridge, created = Fridge.objects.get_or_create(
            user=request.user
        )

        normalized_products = []
        for product in products:
            if not isinstance(product, dict):
                continue

            name = product.get("name")
            quantity = product.get("quantity", 1)
            expire_date = product.get("expire_date")

            if not name:
                continue

            name = str(name).strip()

            if not name:
                continue

            if len(name) > 100:
                name = name[:100]

            try:
                quantity = int(quantity)
            except (ValueError, TypeError):
                quantity = 1

            if quantity < 1:
                quantity = 1
            quantity = min(quantity, 10000)

            parsed_expire_date = None

            if expire_date:
                try:
                    parsed_expire_date = datetime.strptime(
                        str(expire_date),
                        "%Y-%m-%d"
                    ).date()

                    if parsed_expire_date < timezone.localdate():
                        parsed_expire_date = None

                except ValueError:
                    parsed_expire_date = None

            normalized_products.append(Product(
                fridge=fridge,
                name=name,
                quantity=quantity,
                expire_date=parsed_expire_date,
                model_2d=get_product_shape(name)
            ))

        if not normalized_products:
            messages.error(request, "No food products could be identified; your current inventory was kept")
            return redirect("smart-fridge")

        with transaction.atomic():
            fridge.products.all().delete()
            Product.objects.bulk_create(normalized_products)

        messages.success(request, "Your fridge inventory was updated")

        return redirect("smart-fridge")
