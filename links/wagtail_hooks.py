from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.admin.ui.tables import DateColumn
from wagtail.admin.ui.tables.pages import BulkActionsColumn, PageStatusColumn, PageTitleColumn
from wagtail.admin.views.pages.listing import IndexView
from wagtail.admin.viewsets.pages import PageListingViewSet

from links.models import LinkPage


class LinkPageIndexView(IndexView):
    default_ordering = "-last_published_at"


class LinkPageListingViewSet(PageListingViewSet):
    model = LinkPage
    name = "links"
    index_view_class = LinkPageIndexView
    menu_label = "Links"
    menu_icon = "link"
    icon = "link"
    menu_order = 200
    columns = [
        BulkActionsColumn("bulk_actions"),
        PageTitleColumn(
            "title",
            label=_("Title"),
            sort_key="title",
            classname="title",
        ),
        DateColumn(
            "latest_revision_created_at",
            label=_("Updated"),
            sort_key="latest_revision_created_at",
            width="12%",
        ),
        PageStatusColumn(
            "status",
            label=_("Status"),
            sort_key="live",
            width="12%",
        ),
    ]

    search_fields = ("title", "description")
    add_to_admin_menu = True


linkpage_viewset = LinkPageListingViewSet()


@hooks.register("register_admin_viewset")
def register_admin_viewset():
    return linkpage_viewset
