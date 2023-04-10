from datetime import datetime

from django.forms import (
    DateTimeField,
    DateTimeInput,
    ModelForm,
    Textarea,
    URLInput,
    ValidationError,
)
from django.urls import reverse_lazy

from .models import EventPage


class EventSubmissionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = EventPage
        fields = ("description", "link", "start", "end")
        widgets = {
            "link": URLInput,
            "description": Textarea(attrs={"rows": 5}),
            "start": DateTimeInput,
            "end": DateTimeInput,
        }
