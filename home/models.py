from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from taggit.models import Tag as TaggitTag
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet
from wagtailseo.models import SeoMixin


class BasicPage(SeoMixin, Page):
    parent_page_types = ["HomePage"]
    subpage_types = []

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    promote_panels = SeoMixin.seo_meta_panels + SeoMixin.seo_menu_panels

    @cached_property
    def seo_image_url(self):
        if self.og_image:
            image_url = self.og_image.get_rendition("width-1200").url
            return settings.BASE_URL + image_url

        return ""

    @cached_property
    def seo_canonical_url(self):
        return settings.BASE_URL + self.url


class HomePage(SeoMixin, Page):
    subpage_types = ["BasicPage", "links.LinkIndexPage"]

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
        FieldPanel("banner_image"),
        FieldPanel("intro", classname="intro"),
        FieldPanel("body"),
    ]

    promote_panels = SeoMixin.seo_panels

    @cached_property
    def seo_image_url(self):
        if self.og_image:
            image_url = self.og_image.get_rendition("width-1200").url
            return settings.BASE_URL + image_url

        return ""

    @cached_property
    def seo_canonical_url(self):
        return settings.BASE_URL + self.url


@register_snippet
class ModelCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


@register_snippet
class ModelTag(TaggitTag):
    class Meta:
        proxy = True
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name
