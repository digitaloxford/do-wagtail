from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models import Count
from django.shortcuts import redirect, render
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
    subpage_types = ["EventPage", "EventSuggestionPage"]
    max_count = 1

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro", classname="intro"),
    ]

    search_fields = Page.search_fields + [  # Inherit search_fields from Page
        index.SearchField("intro"),
    ]

    promote_panels = SeoMixin.seo_meta_panels + SeoMixin.seo_menu_panels

    def get_template(self, request):
        if request.htmx:
            return "_partials/htmx_events.html"

        return "events/event_index_page.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["events_page"] = self

        # Paginate all events by 20 per page
        paginator = Paginator(self.events, 20)
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
        now = timezone.now()

        return (
            EventPage.objects.descendant_of(self)
            .live()
            .filter(start__gte=now)
            .order_by("-first_published_at")
        )

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

    description = RichTextField(
        verbose_name="Event description",
        features=["h2", "h3", "bold", "italic", "ol", "ul"],
    )

    link = models.URLField(
        verbose_name="Event link",
    )

    start = models.DateTimeField("Starts", blank=False)

    end = models.DateTimeField("Ends", blank=True, null=True)

    location = models.CharField(
        verbose_name="Event location (address)", max_length=1000, blank=True, null=True
    )

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


class EventSuggestionPage(SeoMixin, Page):
    parent_page_types = ["EventIndexPage"]
    subpage_types = []
    max_count = 1

    intro = RichTextField(blank=True)

    thankyou_page_title = models.CharField(
        max_length=255, help_text="Title text to use for the 'thank you' page"
    )

    # Note that there's nothing here for specifying the actual form fields -
    # those are still defined in forms.py. There's no benefit to making these
    # editable within the Wagtail admin, since you'd need to make changes to
    # the code to make them work anyway.

    content_panels = Page.content_panels + [
        FieldPanel("intro", classname="full"),
        FieldPanel("thankyou_page_title"),
    ]

    promote_panels = SeoMixin.seo_meta_panels + SeoMixin.seo_menu_panels

    def serve(self, request):
        from .forms import EventSubmissionForm

        if request.method == "POST":
            form = EventSubmissionForm(request.POST)
            if form.is_valid():
                event = form.save()
                return render(
                    request,
                    "events/event_thankyou.html",
                    {
                        "page": self,
                        "event": event,
                    },
                )
        else:
            form = EventSubmissionForm()

        return render(
            request,
            "events/event_suggestion.html",
            {
                "page": self,
                "form": form,
            },
        )


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
