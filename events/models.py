import datetime

import pytz
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models import Count
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.functional import cached_property
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index
from wagtailseo.models import SeoMixin

from home.models import ModelCategory


class EventIndexPage(RoutablePageMixin, SeoMixin, Page):
    # Set parent_page_types to an empty list to prevent it from
    # being created in the editor interface.
    parent_page_types = ["home.HomePage"]
    subpage_types = ["EventPage"]
    max_count = 1

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro", classname="intro"),
    ]

    search_fields = Page.search_fields + [  # Inherit search_fields from Page
        index.SearchField("intro"),
    ]

    promote_panels = SeoMixin.seo_meta_panels + SeoMixin.seo_menu_panels

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["events_page"] = self

        now = timezone.now()

        all_events = (
            EventPage.objects.all()
            .specific()
            .live()
            .filter(start__gte=now)
            .order_by("-first_published_at")
        )

        # Paginate all events by 20 per page
        paginator = Paginator(all_events, 20)
        # Try to get the ?page=x value
        page = request.GET.get("page")

        try:
            # If the page exists and the ?page=x is an int
            events = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            events = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            events = paginator.page(paginator.num_pages)

        context["events"] = events

        # Get active categories
        categories = (
            ModelCategory.objects.annotate(exists=Count("event_pages"))
            .filter(exists__gt=0)
            .order_by("name")
        )

        context["categories"] = categories

        return context

    def get_events(self):
        return EventPage.objects.descendant_of(self).live().order_by("title")

    @route(r"^$")
    def event_list(self, request, *args, **kwargs):
        self.events = self.get_events()
        return self.render(request)

    @route(r"^category/(?P<category>[-\w]+)/$")
    def post_by_category(self, request, category, *args, **kwargs):
        category_name = ModelCategory.objects.values_list("name", flat=True).get(
            slug=category
        )

        self.filter_type = "category"
        self.filter_slug = category
        self.filter_term = category_name
        self.events = self.get_events().filter(
            categories__event_category__slug=category
        )

        return self.render(request)

    @cached_property
    def seo_image_url(self):
        if self.og_image:
            image_url = self.og_image.get_rendition("width-1200").url
            return settings.BASE_URL + image_url

        return ""

    @cached_property
    def seo_canonical_url(self):
        return settings.BASE_URL + self.url


class EventPage(SeoMixin, Page):
    parent_page_types = ["EventIndexPage"]
    subpage_types = []

    link = models.URLField()

    description = RichTextField(
        verbose_name="Long description",
        features=["h2", "h3", "bold", "italic", "ol", "ul"],
    )

    start = models.DateTimeField("Starts", blank=False)

    end = models.DateTimeField("End", blank=True, null=True)

    location = models.CharField(max_length=1000, blank=True, null=True)

    tags = ClusterTaggableManager(through="events.EventPageTag", blank=True)

    event_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("event_image", help_text="I dunno, a logo maybe?"),
        FieldPanel("description", classname="full"),
        MultiFieldPanel(
            [
                FieldPanel("location"),
                FieldPanel("link"),
                FieldPanel("start"),
                FieldPanel("end"),
            ],
            heading="Event details",
        ),
        MultiFieldPanel(
            [
                InlinePanel(
                    "categories",
                    label="category",
                ),
                FieldPanel("tags"),
            ],
            heading="Metadata",
        ),
    ]

    promote_panels = SeoMixin.seo_meta_panels + SeoMixin.seo_menu_panels

    search_fields = Page.search_fields + [  # Inherit search_fields from Page
        index.SearchField("description"),
        index.FilterField("tags"),
        index.FilterField("categories"),
    ]

    class Meta:
        ordering = ["title"]
        verbose_name = "Event"
        verbose_name_plural = "Events"


class EventPageCategory(models.Model):
    page = ParentalKey(
        "events.EventPage", on_delete=models.CASCADE, related_name="categories"
    )
    event_category = models.ForeignKey(
        "home.ModelCategory", on_delete=models.CASCADE, related_name="event_pages"
    )

    panels = [
        FieldPanel("event_category"),
    ]

    class Meta:
        unique_together = ("page", "event_category")


class EventPageTag(TaggedItemBase):
    content_object = ParentalKey("EventPage", related_name="tagged_items")
