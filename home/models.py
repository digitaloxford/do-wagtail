from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from wagtailmetadata.models import MetadataPageMixin

from jobs.models import JobIndexPage


@register_setting
class SocialMediaSettings(BaseSetting):
    twitter = models.CharField(max_length=100, help_text="Twitter Username", blank=True)


class BasicPage(MetadataPageMixin, Page):
    parent_page_types = ["HomePage"]
    subpage_types = []

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body", classname="full"),
    ]


class HomePage(MetadataPageMixin, Page):
    subpage_types = ["BasicPage", "jobs.JobIndexPage"]

    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel("banner_image"),
        FieldPanel("intro", classname="intro"),
        FieldPanel("body", classname="full"),
    ]
