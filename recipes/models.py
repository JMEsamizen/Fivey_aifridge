from django.db import models


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
