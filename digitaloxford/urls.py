from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("users.urls")),
    # path("jobs/", include("jobs.urls"), name="jobs"),
    # Service worker
    url(
        r"^serviceworker.js",
        (
            TemplateView.as_view(
                template_name="serviceworker.js",
                content_type="application/javascript",
            )
        ),
        name="serviceworker.js",
    ),
    # Microsoft Tile config
    url(
        r"^browserconfig.xml",
        (
            TemplateView.as_view(
                template_name="browserconfig.xml",
                content_type="application/xml",
            )
        ),
        name="browserconfig.xml",
    ),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r"", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
