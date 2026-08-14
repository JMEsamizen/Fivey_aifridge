from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    birth_date = models.DateField(
        null=True,
        blank=True
    )

    surname = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        validators=[
            MinLengthValidator(2)
        ]
    )

    def __str__(self):
        return self.user.username