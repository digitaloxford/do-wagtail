from datetime import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.urls import reverse_lazy

from .models import EventPage


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # self.helper.form_action = reverse_lazy('index')
        # self.helper.form_method = 'POST'
        self.helper.form_id = "event-submission-form"
        self.helper.attrs = {
            "hx-post": reverse_lazy("index"),
            "hx-target": "#event-submission-form",
            "hx-swap": "outerHTML",
        }
        self.helper.add_input(Submit("submit", "Submit"))

    class Meta:
        model = EventPage
        fields = ("link" "description", "start", "end", "location", "event_image")

    # def clean_username(self):
    #     username = self.cleaned_data["username"]
    #     if len(username) <= 3:
    #         raise forms.ValidationError("Username is too short")
    #     return username

    def save(self, commit=True):
        event = super().save(commit=False)

        if commit:
            event.save()
        return event
