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