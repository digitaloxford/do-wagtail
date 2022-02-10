from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models import Count
from django.shortcuts import redirect
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtailseo.models import SeoMixin

from home.models import ModelCategory


class LinkIndexPage(RoutablePageMixin, SeoMixin, Page):
    # Set parent_page_types to an empty list to prevent it from
    # being created in the editor interface.
    # parent_page_types = []
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

        # https://docs.djangoproject.com/en/3.1/topics/pagination/#using-paginator-in-a-view-function
        paginator = Paginator(self.links, 10)
        page = request.GET.get("page")
        try:
            links = paginator.page(page)
        except PageNotAnInteger:
            links = paginator.page(1)
        except EmptyPage:
            links = paginator.object_list.none()

        context["links"] = links

        # Get active categories
        categories = (
            ModelCategory.objects.annotate(exists=Count("link_pages"))
            .filter(exists__gt=0)
            .order_by("name")
        )

        context["categories"] = categories

        return context

    def get_links(self):
        return LinkPage.objects.descendant_of(self).live().order_by("title")

    @route(r"^$")
    def link_list(self, request, *args, **kwargs):
        self.links = self.get_links()
        return self.render(request)

    @route(r"^category/(?P<category>[-\w]+)/$")
    def post_by_category(self, request, category, *args, **kwargs):
        category_name = ModelCategory.objects.values_list("name", flat=True).get(
            slug=category
        )

        self.filter_type = "category"
        self.filter_slug = category
        self.filter_term = category_name
        self.links = self.get_links().filter(categories__link_category__slug=category)

        return self.render(request)


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
        ImageChooserPanel("link_image", help_text="I dunno, a logo maybe?"),
        FieldPanel("link", classname="full"),
        FieldPanel("description", classname="full"),
        FieldPanel("testimonial", classname="full"),
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
    page = ParentalKey(
        "links.LinkPage", on_delete=models.CASCADE, related_name="categories"
    )
    link_category = models.ForeignKey(
        "home.ModelCategory", on_delete=models.CASCADE, related_name="link_pages"
    )

    panels = [
        SnippetChooserPanel("link_category"),
    ]

    class Meta:
        unique_together = ("page", "link_category")


class LinkPageTag(TaggedItemBase):
    content_object = ParentalKey("LinkPage", related_name="tagged_items")
