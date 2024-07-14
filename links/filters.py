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
        choices=category_choice,
        widget=forms.Select(
            # attrs={
            #     "hx-target": "ul.h-feed",
            #     "hx-swap": "outerHTML",
            #     "hx-get": reverse_lazy("shutdowns"),
            #     "hx-push-url": "true",
            # }
        ),
    )

    class Meta:
        model = LinkPage
        fields = ["category"]

    # def universal_search(self, queryset, name, value):
    #     return ShutdownIncident.objects.filter(Q(participant__icontains=value))
