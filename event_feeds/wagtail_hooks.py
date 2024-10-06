# event_feeds/wagtail_hooks.py
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import EventFeed


class EventFeedAdmin(ModelAdmin):
    model = EventFeed
    menu_label = 'Event Feeds'
    menu_icon = 'site'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name', 'url', 'last_updated')
    search_fields = ('name', 'url')

modeladmin_register(EventFeedAdmin)
