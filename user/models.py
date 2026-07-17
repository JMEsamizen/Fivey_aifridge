from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    surname = models.CharField(max_length=30, null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    
class Fridge(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="fridge"
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s fridge"


class Product(models.Model):
    fridge = models.ForeignKey(
        Fridge,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name