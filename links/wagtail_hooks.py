from django.urls import reverse
from wagtail import hooks
from wagtail.admin.menu import AdminOnlyMenuItem, MenuItem
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import LinkPage


# Hide links for non admins
@hooks.register("construct_main_menu")
def hide_admin_items_from_users(request, menu_items):
    if request.user.is_staff is not True:
        menu_items[:] = [item for item in menu_items if item.name not in ["links"]]


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
