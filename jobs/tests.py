from wagtail.tests.utils import WagtailPageTests

from home.models import BasicPage, HomePage

from .models import JobIndexPage, JobPage


class JobIndexPageTests(WagtailPageTests):
    def test_can_create_under_home_page(self):
        # You can create a JobIndexPage under the HomePage
        self.assertCanCreateAt(HomePage, JobIndexPage)

    def test_cant_create_under_basic_page(self):
        # You can not create a JobIndexPage under a BasicPage
        self.assertCanNotCreateAt(BasicPage, JobIndexPage)


class JobPageTests(WagtailPageTests):
    def test_can_create_under_job_index_page(self):
        # You can create a JobPage under a JobIndexPage
        self.assertCanCreateAt(JobIndexPage, JobPage)

    def test_cant_create_under_home_page(self):
        # You can not create a JobPage under the HomePage
        self.assertCanNotCreateAt(HomePage, JobPage)

    def test_job_page_parent_pages(self):
        # A JobPage can only be created under a JobIndexPage
        self.assertAllowedParentPageTypes(JobPage, {JobIndexPage})
