from wagtail.test.utils import WagtailPageTestCase

from jobs.models import JobIndexPage
from links.models import LinkIndexPage

from .models import BasicPage, HomePage


class HomePageTests(WagtailPageTestCase):
    def test_home_page_subpages(self):
        # A HomePage can only have other BasicPage and *IndexPage children
        self.assertAllowedSubpageTypes(
            HomePage, {BasicPage, LinkIndexPage, JobIndexPage}
        )

    def test_cant_create_under_basic_page(self):
        # You can not create a HomePage under a BasicPage
        self.assertCanNotCreateAt(BasicPage, HomePage)


class BasicPageTests(WagtailPageTestCase):
    def test_can_create_under_home_page(self):
        # You can create a BasicPage under a HomePage
        self.assertCanCreateAt(HomePage, BasicPage)

    def test_cant_create_under_link_index_page(self):
        # You can not create a BasicPage under the LinkIndexPage
        self.assertCanNotCreateAt(BasicPage, LinkIndexPage)

    def test_cant_create_under_job_index_page(self):
        # You can not create a BasicPage under the JobIndexPage
        self.assertCanNotCreateAt(BasicPage, JobIndexPage)
