from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail.core import hooks
from wagtail.snippets.wagtail_hooks import SnippetsMenuItem

from .models import ModelCategory, ModelTag


# Hide default snippets menu as we're recreating it to gain access to custom listing pages
@hooks.register("construct_main_menu")
def hide_snippets_menu_item(request, menu_items):
    menu_items[:] = [
        item for item in menu_items if not isinstance(item, SnippetsMenuItem)
    ]


class ModelCategoryAdmin(ModelAdmin):
    """Category model admin."""

    model = ModelCategory
    menu_icon = "list-ul"
    menu_order = 230
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")
    ordering = ["name"]


class ModelTagAdmin(ModelAdmin):
    """Tag model admin."""

    model = ModelTag
    menu_icon = "list-ul"
    menu_order = 230
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")
    ordering = ["name"]


class SnippetGroup(ModelAdminGroup):
    menu_label = "Snippets"
    menu_icon = "folder-open-inverse"
    menu_order = 300  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (
        ModelCategoryAdmin,
        ModelTagAdmin,
    )


modeladmin_register(SnippetGroup)
