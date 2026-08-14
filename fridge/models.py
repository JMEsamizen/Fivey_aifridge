from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class FridgeItem(models.Model):
    title = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2)
        ]
    )

    description = models.TextField(
        validators=[
            MinLengthValidator(2)
        ]
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "fridge_items"


class Fridge(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="fridge"
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username}'s fridge"


class Product(models.Model):
    fridge = models.ForeignKey(
        Fridge,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2)
        ]
    )

    quantity = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1)
        ]
    )

    # These fields already exist in the production database from an earlier
    # version of the product model. Defaults keep both old and fresh databases
    # compatible while nutrition analysis is optional.
    calories = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    benefits = models.TextField(blank=True, default="")
    warnings = models.TextField(blank=True, default="")

    model_2d = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    expire_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def clean(self):
        super().clean()

        if self.expire_date and self.expire_date < timezone.localdate():
            raise ValidationError({
                "expire_date": "Expiration date cannot be in the past."
            })

        if self.name and not self.name.strip():
            raise ValidationError({
                "name": "Product name cannot be empty."
            })

    def __str__(self):
        return self.name


class ExpiryNotification(models.Model):
    TWO_DAYS = "two_days"
    TODAY = "today"
    TYPE_CHOICES = [
        (TWO_DAYS, "Expires in two days"),
        (TODAY, "Expires today"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expiry_notifications")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="expiry_notifications")
    product_name = models.CharField(max_length=100)
    expire_date = models.DateField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product", "expire_date", "notification_type"],
                name="unique_product_expiry_notification",
            )
        ]

    def __str__(self):
        return self.message
