from django.conf.urls import include, url
from registration.views import RegistrationView

from . import views
from .forms import RecruiterRegistrationForm

# urlpatterns = [
#     url(
#         r"^register/$",
#         RegistrationView.as_view(form_class=RecruiterRegistrationForm),
#         name="registration_register",
#     ),
#     url(r"^", include("registration.backends.admin_approval.urls")),
# ]
