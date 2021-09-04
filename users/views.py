from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic

from . import models


def profile_view(request):
    return render(request, "users/profile.html")
