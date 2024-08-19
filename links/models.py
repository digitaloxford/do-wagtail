from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models import Prefetch
from django.shortcuts import render
from django.utils.functional import cached_property
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index
from wagtailseo.models import SeoMixin


class LinkIndexPage(RoutablePageMixin, SeoMixin, Page):
    # Set parent_page_types to an empty list to prevent it from
    # being created in the editor interface.
    parent_page_types = ["home.HomePage"]
    subpage_types = ["LinkPage"]
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
        context["links_page"] = self

        # Prevent circular import
        # TODO: I could just define the filter in models.py
        from .filters import LinkFilter

        links_list = LinkPage.objects.descendant_of(self).live().order_by("title").prefetch_related(
            Prefetch(
                'categories',
                queryset=LinkPageCategory.objects.select_related('link_category'),
                to_attr='prefetched_categories'
            )
        )

        queryset = links_list
        link_page_filter = LinkFilter(request.GET, queryset=queryset)
        filtered_queryset = link_page_filter.qs

        page = request.GET.get("page")
        paginator = Paginator(filtered_queryset, 1000)

        try:
            links = paginator.page(page)
        except PageNotAnInteger:
            links = paginator.page(1)
        except EmptyPage:
            links = paginator.object_list.none()

        context["filter"] = link_page_filter
        context["links"] = links

        return context

    def serve(self, request, *args, **kwargs):
        # Override the Page.serve() method if it's a HTMX request.
        # In Django this would normally go in your views.py file

        if request.htmx:
            context = self.get_context(request, *args, **kwargs)
            if "links" in context:
                result_dict = {"links": context["links"], "filter": context["filter"]}
                return render(request, "links/link_index_page.html#links-results", result_dict)
            else:
                result_dict = {"links": None, "filter": context["filter"]}
                return render(request, "links/link_index_page.html#links-results", result_dict)
        else:
            return super().serve(request, *args, **kwargs)

    def get_links(self):
        return LinkPage.objects.descendant_of(self).live().order_by("title")

    @cached_property
    def seo_image_url(self):
        if self.og_image:
            image_url = self.og_image.get_rendition("width-1200").url
            return settings.BASE_URL + image_url

        return ""

    @cached_property
    def seo_canonical_url(self):
        return settings.BASE_URL + self.url


class LinkPage(Page):
    parent_page_types = ["LinkIndexPage"]

    link = models.URLField()

    description = models.CharField(max_length=1000)

    testimonial = models.CharField(max_length=1000, blank=True)

    tags = ClusterTaggableManager(through="links.LinkPageTag", blank=True)

    link_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("link_image", help_text="I dunno, a logo maybe?"),
        FieldPanel("link"),
        FieldPanel("description"),
        FieldPanel("testimonial"),
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

    search_fields = Page.search_fields + [  # Inherit search_fields from Page
        index.SearchField("description"),
        index.FilterField("tags"),
        index.FilterField("categories"),
    ]

    class Meta:
        ordering = ["title"]
        verbose_name = "Link"
        verbose_name_plural = "Links"


class LinkPageCategory(models.Model):
    page = ParentalKey("links.LinkPage", on_delete=models.CASCADE, related_name="categories")
    link_category = models.ForeignKey("home.ModelCategory", on_delete=models.CASCADE, related_name="link_pages")

    panels = [
        FieldPanel("link_category"),
    ]

    class Meta:
        unique_together = ("page", "link_category")


class LinkPageTag(TaggedItemBase):
    content_object = ParentalKey("LinkPage", related_name="tagged_items")
