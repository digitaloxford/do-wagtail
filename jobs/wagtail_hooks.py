from django.urls import path, reverse
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.admin.ui.sidebar import LinkMenuItem as LinkMenuItemComponent
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import JobPage, RecruiterPage


class EditAccountMenuItem(MenuItem):
    """Edit account link for logged in user"""

    def is_shown(self, request):
        # Hide from non admin users
        return request.user.is_staff is not True


@hooks.register("register_admin_menu_item")
def register_account_menu_item():
    return EditAccountMenuItem(
        "Account Settings", "/admin/account", classnames="icon icon-user", order=100
    )


class EditProfileMenuItem(MenuItem):
    """Retrieve RecruiterPage for logged in user"""

    def is_shown(self, request):
        # Hide from non admin users
        return request.user.is_staff is not True

    def render_component(self, request):
        # Get url to profile page
        edit_link = None
        if request.user.owned_pages.exists():
            for page in request.user.owned_pages.type(RecruiterPage):
                if page.id:
                    edit_link = "/admin/pages/" + str(page.id) + "/edit/"

                    return LinkMenuItemComponent(
                        self.name,
                        self.label,
                        url=edit_link,
                        icon_name=self.icon_name,
                        classnames=self.classnames,
                        attrs=self.attrs,
                    )


@hooks.register("register_admin_menu_item")
def register_profile_menu_item():
    return EditProfileMenuItem(
        "Public Profile", "", classnames="icon icon-view", order=50
    )


class JobPageModelAdmin(ModelAdmin):
    """JobPage model admin."""

    model = JobPage
    menu_label = "Job Posts"
    menu_icon = "list-ul"
    menu_order = 10
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title", "short_description", "closing_date")
    search_fields = ("title",)
    ordering = ["closing_date"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # If admin show full listing
        if request.user.is_staff:
            return qs
        else:
            # Only show jobs owned by the current user
            return qs.filter(owner_id=request.user.id)


modeladmin_register(JobPageModelAdmin)
