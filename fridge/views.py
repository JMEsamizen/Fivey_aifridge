from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.urls import reverse
from django.utils import timezone
from django.db import transaction
from datetime import datetime
from math import isfinite
from PIL import Image, UnidentifiedImageError

from .models import ExpiryNotification, Fridge, Product
from .additional_func import get_product_shape
from fridge.ai_utils import analyze_media, AIServiceError
from .services import create_expiry_notifications

from django.contrib import messages


def normalized_nutrition_value(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return 0

    return min(value, 100000) if isfinite(value) and value > 0 else 0


def normalized_text(value, limit=300):
    return str(value).strip()[:limit] if value else ""

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


class ProductUpdateView(View):

    def post(self, request, product_id):
        if not request.user.is_authenticated:
            messages.info(request, "Sign in to analyze your fridge photo.")
            return redirect(f"{reverse('login')}?next={request.path}")

        product = get_object_or_404(
            Product,
            pk=product_id,
            fridge__user=request.user,
        )

        name = request.POST.get("name", "").strip()
        quantity = request.POST.get("quantity", "1")
        expire_date = request.POST.get("expire_date", "")

        if not name or len(name) > 100:
            messages.error(request, "Product name must contain 1 to 100 characters")
            return redirect("smart-fridge")

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            messages.error(request, "Quantity must be a number")
            return redirect("smart-fridge")

        if not 1 <= quantity <= 10000:
            messages.error(request, "Quantity must be between 1 and 10,000")
            return redirect("smart-fridge")

        parsed_expire_date = None
        if expire_date:
            try:
                parsed_expire_date = datetime.strptime(expire_date, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, "Invalid expiration date")
                return redirect("smart-fridge")

            if parsed_expire_date < timezone.localdate():
                messages.error(request, "Expiration date cannot be in the past")
                return redirect("smart-fridge")

        name_changed = product.name.casefold() != name.casefold()
        expiry_changed = product.expire_date != parsed_expire_date
        product.name = name
        product.quantity = quantity
        product.expire_date = parsed_expire_date
        product.model_2d = get_product_shape(name)

        if name_changed:
            product.calories = 0
            product.protein = 0
            product.carbs = 0
            product.fat = 0
            product.benefits = ""
            product.warnings = ""

        product.save()
        if name_changed or expiry_changed:
            product.expiry_notifications.all().delete()
        messages.success(request, "Product updated")
        return redirect("smart-fridge")


class ProductDeleteView(View):

    def post(self, request, product_id):
        if not request.user.is_authenticated:
            return redirect("login")

        product = get_object_or_404(
            Product,
            pk=product_id,
            fridge__user=request.user,
        )
        product.expiry_notifications.all().delete()
        product.delete()
        messages.success(request, "Product deleted")
        return redirect("smart-fridge")


class ExpiryNotificationOpenView(View):

    def get(self, request, notification_id):
        if not request.user.is_authenticated:
            return redirect("login")

        notification = get_object_or_404(
            ExpiryNotification,
            pk=notification_id,
            user=request.user,
        )
        if notification.read_at is None:
            notification.read_at = timezone.now()
            notification.save(update_fields=["read_at"])

        return redirect(f"/recipes/suggestions/?product={notification.product_name}")


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
        create_expiry_notifications()

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
                "fridge": fridge,
                "expiry_notifications": ExpiryNotification.objects.filter(
                    user=request.user,
                    read_at__isnull=True,
                )[:5],
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

        try:
            products = analyze_media(file)
        except AIServiceError as exc:
            messages.error(request, f"AI could not analyze this image: {exc}")
            return redirect("smart-fridge")

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
                model_2d=get_product_shape(name),
                calories=normalized_nutrition_value(product.get("calories")),
                protein=normalized_nutrition_value(product.get("protein")),
                carbs=normalized_nutrition_value(product.get("carbs")),
                fat=normalized_nutrition_value(product.get("fat")),
                benefits=normalized_text(product.get("benefits")),
                warnings=normalized_text(product.get("warnings")),
            ))

        if not normalized_products:
            messages.error(request, "No food products could be identified; your current inventory was kept")
            return redirect("smart-fridge")

        with transaction.atomic():
            ExpiryNotification.objects.filter(
                user=request.user,
                product__fridge=fridge,
            ).delete()
            fridge.products.all().delete()
            Product.objects.bulk_create(normalized_products)

        messages.success(request, "Your fridge inventory was updated")

        return redirect("smart-fridge")
