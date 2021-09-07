from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    display_name = models.CharField(
        verbose_name="Display name",
        max_length=100,
    )

    class Meta:
        ordering = ["display_name"]

    def get_absolute_url(self):
        return reverse("users_profile")

    def __str__(self):
        return f"{self.username}"
