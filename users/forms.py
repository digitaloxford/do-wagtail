from django import forms
from django.db import models
from wagtail.users.forms import UserCreationForm, UserEditForm

from .models import User


class WagtailUserEditForm(UserEditForm):
    display_name = models.CharField(
        verbose_name="Display name",
        max_length=100,
    )

    class Meta(UserEditForm.Meta):
        model = User


class WagtailUserCreationForm(UserCreationForm):
    display_name = models.CharField(
        verbose_name="Display name",
        max_length=100,
    )

    class Meta(UserCreationForm.Meta):
        model = User
