from django.db import models
from taggit.models import Tag as TaggitTag
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from wagtail.snippets.models import register_snippet
from wagtailseo.models import SeoMixin


class BasicPage(SeoMixin, Page):
    parent_page_types = ["HomePage"]
    subpage_types = []

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body", classname="full"),
    ]

    promote_panels = SeoMixin.seo_meta_panels + SeoMixin.seo_menu_panels


class HomePage(SeoMixin, Page):
    subpage_types = ["BasicPage", "jobs.JobIndexPage", "links.LinkIndexPage"]

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

    promote_panels = SeoMixin.seo_panels


@register_snippet
class ModelCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


@register_snippet
class ModelTag(TaggitTag):
    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
