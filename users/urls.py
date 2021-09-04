from django.urls import include, path, re_path

from . import views

urlpatterns = [path("profile/", views.profile_view, name="users_profile")]
