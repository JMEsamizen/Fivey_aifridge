from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from datetime import datetime

from .models import Fridge, Product
from .additional_func import get_product_shape
from fridge.ai_utils import analyze_media

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
            return render(
                request,
                "fridge/my_fridge.html",
                {"error": "Product name is too long"}
            )

        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            return render(
                request,
                "fridge/my_fridge.html",
                {"error": "Quantity must be a number"}
            )

        if quantity < 1:
            return render(
                request,
                "fridge/my_fridge.html",
                {"error": "Quantity must be at least 1"}
            )

        parsed_expire_date = None

        if expire_date:
            try:
                parsed_expire_date = datetime.strptime(
                    expire_date,
                    "%Y-%m-%d"
                ).date()
            except ValueError:
                return render(
                    request,
                    "fridge/my_fridge.html",
                    {"error": "Invalid expiration date"}
                )

            if parsed_expire_date < timezone.localdate():
                return render(
                    request,
                    "fridge/my_fridge.html",
                    {"error": "Expiration date cannot be in the past"}
                )

        fridge, created = Fridge.objects.get_or_create(
            user=request.user
        )

        product = Product.objects.create(
            fridge=fridge,
            name=name,
            quantity=quantity,
            expire_date=parsed_expire_date,
            model_2d=get_product_shape(name)
        )

        return render(
            request,
            "fridge/my_fridge.html",
            {
                "product": product
            }
        )


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
            return render(
                request,
                "fridge/smartfridges.html",
                {
                    "error": "Image size must be less than 10 MB"
                }
            )

        products = analyze_media(file)

        if not isinstance(products, list):
            return render(
                request,
                "fridge/smartfridges.html",
                {
                    "error": "Could not analyze the image"
                }
            )

        fridge, created = Fridge.objects.get_or_create(
            user=request.user
        )

        fridge.products.all().delete()

        for product in products:

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

            Product.objects.create(
                fridge=fridge,
                name=name,
                quantity=quantity,
                expire_date=parsed_expire_date,
                model_2d=get_product_shape(name)
            )

        return redirect("smart-fridge")