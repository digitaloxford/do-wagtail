from datetime import timezone

from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page


class EventFeed(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    last_updated = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]

    def __str__(self):
        return self.name


class Event(models.Model):
    feed = models.ForeignKey(EventFeed, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title


class EventListPage(Page):
    intro = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['events'] = Event.objects.filter(start_date__gte=timezone.now()).order_by('start_date')
        return context
