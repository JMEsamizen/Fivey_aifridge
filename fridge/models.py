from django.db import models
from django.contrib.auth.models import User

class FridgeItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    model_3d = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

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

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s fridge"


class Product(models.Model):
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name