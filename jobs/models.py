import json

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils import timezone
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtailseo.models import SeoMixin
from wagtailseo.utils import StructDataEncoder, get_struct_data_images

from users.models import User


class JobIndexPage(SeoMixin, Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["RecruiterPage"]
    max_count = 1

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro", classname="intro"),
    ]

    promote_panels = SeoMixin.seo_panels

    def get_context(self, request):
        # Update context to include only published jobs, ordered
        # reverse-chronologically
        context = super().get_context(request)
        now = timezone.now()

        all_jobs = (
            JobPage.objects.all()
            .specific()
            .live()
            .filter(closing_date__gte=now)
            .order_by("-first_published_at")
        )

        # Paginate all jobs by 20 per page
        paginator = Paginator(all_jobs, 20)
        # Try to get the ?page=x value
        page = request.GET.get("page")

        try:
            # If the page exists and the ?page=x is an int
            jobs = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            jobs = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            jobs = paginator.page(paginator.num_pages)

        context["jobs"] = jobs
        return context


class RecruiterPage(SeoMixin, Page):
    parent_page_types = ["JobIndexPage"]
    subpage_types = ["JobPage"]

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(
        "Description",
        help_text="A little bit about yourself (don't be spammy)",
        max_length=4096,
        blank=True,
        null=True,
    )
    website = models.URLField(verbose_name="Website", blank=True, null=True)
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    phone = models.CharField(
        verbose_name="Phone",
        max_length=17,
        blank=True,
        null=True,
    )
    address1 = models.CharField(
        verbose_name="Address line 1", max_length=1024, blank=True, null=True
    )
    address2 = models.CharField(
        verbose_name="Address line 2", max_length=1024, blank=True, null=True
    )
    postal_code = models.CharField(
        verbose_name="Postal Code", max_length=12, blank=True, null=True
    )
    city = models.CharField(verbose_name="City", max_length=1024, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("description", classname="full"),
        MultiFieldPanel(
            [
                FieldPanel("website"),
                FieldPanel("email"),
                FieldPanel("phone"),
            ],
            heading="Contact details",
        ),
        MultiFieldPanel(
            [
                FieldPanel("address1"),
                FieldPanel("address2"),
                FieldPanel("postal_code"),
                FieldPanel("city"),
            ],
            heading="Address",
        ),
    ]

    promote_panels = SeoMixin.seo_panels

    def get_context(self, request):
        # Update context to include jobs by this recruiter
        context = super().get_context(request)
        now = timezone.now()

        all_jobs = (
            JobPage.objects.child_of(self)
            .specific()
            .live()
            .filter(closing_date__gte=now)
            .order_by("-first_published_at")
        )

        # Paginate all jobs by 20 per page
        paginator = Paginator(all_jobs, 20)
        # Try to get the ?page=x value
        page = request.GET.get("page")

        try:
            # If the page exists and the ?page=x is an int
            jobs = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            jobs = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            jobs = paginator.page(paginator.num_pages)

        context["jobs"] = jobs
        return context

    class Meta:
        ordering = ["title"]


class JobTag(TaggedItemBase):
    content_object = ParentalKey(
        "JobPage", related_name="tagged_items", on_delete=models.CASCADE
    )


class JobPage(SeoMixin, Page):
    parent_page_types = ["RecruiterPage"]
    subpage_types = []

    JOB_TYPE_PERMANENT = "permanent"
    JOB_TYPE_CONTRACT = "contract"
    JOB_TYPE_TEMPORARY = "temporary"
    JOB_TYPE_FREELANCE = "freelance"

    JOB_TYPES = (
        (JOB_TYPE_PERMANENT, "Permanent"),
        (JOB_TYPE_CONTRACT, "Contract"),
        (JOB_TYPE_TEMPORARY, "Temporary"),
        (JOB_TYPE_FREELANCE, "Freelance"),
    )
    short_description = models.CharField(
        max_length=500,
        help_text="A brief description of the job, One or two sentences at most.",
    )
    description = RichTextField(
        verbose_name="Long description",
        features=["h2", "h3", "bold", "italic", "ol", "ul"],
    )
    job_type = models.CharField(
        max_length=300,
        choices=JOB_TYPES,
        default=JOB_TYPE_PERMANENT,
    )
    salary = models.CharField(verbose_name="Salary / Rate", max_length=1024)
    closing_date = models.DateField()
    job_link = models.URLField()
    email = models.EmailField(max_length=254)
    tags = ClusterTaggableManager(through=JobTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("short_description"),
        FieldPanel("description"),
        FieldPanel("job_type"),
        FieldPanel("salary"),
        FieldPanel("closing_date"),
        FieldPanel("job_link", heading="Link to apply for this position"),
        FieldPanel("email", heading="Email address for more information"),
    ]

    promote_panels = SeoMixin.seo_panels

    # Wagtail SEO fallback sources
    seo_pagetitle_sources = [
        "title",
    ]

    seo_description_sources = [
        "search_description",
        "short_description",
    ]

    @property
    def my_struct_job_dict(self) -> dict:
        sd_dict = {
            "@context": "https://schema.org/",
            "@type": "JobPosting",
            "title": self.title,
            "description": self.short_description,
            "datePosted": self.seo_published_at,
            "baseSalary": self.salary,
            "salaryCurrency": "GBP",
            "employmentType": self.job_type,
            "applicationContact": self.email,
            "directApply": self.job_link,
        }

        return sd_dict

    @property
    def my_struct_job_json(self) -> str:
        return json.dumps(self.my_struct_job_dict, cls=StructDataEncoder)

    class Meta:
        ordering = ["title"]
        verbose_name = "Job"
        verbose_name_plural = "Jobs"
