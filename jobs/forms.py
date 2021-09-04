from allauth.account.forms import SignupForm
from django import forms
from django.db import models


class RecruiterRegistrationForm(SignupForm):
    display_name = forms.CharField(
        help_text="Used for your public profile page on Digital Oxford. Maximum 100 characters",
        max_length=100,
    )

    first_name = forms.CharField(
        help_text="Used for your account on Digital Oxford. Maximum 100 characters",
        max_length=100,
    )

    last_name = forms.CharField(
        help_text="Used for your account on Digital Oxford. Maximum 100 characters",
        max_length=100,
    )

    # Override the init method
    def __init__(self, *args, **kwargs):
        # Call the init of the parent class
        super().__init__(*args, **kwargs)
        # Remove autofocus because it is in the wrong place
        # del self.fields["username"].widget.attrs["autofocus"]

    def save(self, request):
        user = super(RecruiterRegistrationForm, self).save(request)
        user.display_name = self.cleaned_data["display_name"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user
