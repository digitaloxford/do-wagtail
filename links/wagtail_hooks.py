from wagtail.admin.menu import MenuItem
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.core import hooks

from .models import LinkPage


class LinkPageModelAdmin(ModelAdmin):
    """LinkPage model admin."""

    model = LinkPage
    menu_label = "Links"
    menu_icon = "link"
    menu_order = 15
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title", "description")
    search_fields = ("title", "description")


modeladmin_register(LinkPageModelAdmin)
