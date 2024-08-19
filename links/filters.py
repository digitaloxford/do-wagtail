import django_filters
from django import forms
from django.db.models import Count

from home.models import ModelCategory

from .models import LinkPage

category_choice = (
    ModelCategory.objects.annotate(exists=Count("link_pages"))
    .filter(exists__gt=0)
    .order_by("name")
    .values_list("slug", "name")
)


class LinkFilter(django_filters.FilterSet):
    category = django_filters.ChoiceFilter(
        label="Category",
        field_name="categories__link_category__slug",
        empty_label="-- All --",
        required=False,
        choices=category_choice,
        widget=forms.Select(),
    )

    class Meta:
        model = LinkPage
        fields = ["category"]
