from wagtail.test.utils import WagtailPageTestCase

from home.models import BasicPage, HomePage

from .models import LinkIndexPage, LinkPage


class LinkIndexPageTests(WagtailPageTestCase):
    def test_can_create_under_home_page(self):
        # You can create a LinkIndexPage under the HomePage
        self.assertCanCreateAt(HomePage, LinkIndexPage)

    def test_cant_create_under_basic_page(self):
        # You can not create a LinkIndexPage under a BasicPage
        self.assertCanNotCreateAt(BasicPage, LinkIndexPage)


class LinkPageTests(WagtailPageTestCase):
    def test_can_create_under_link_index_page(self):
        # You can create a LinkPage under a LinkIndexPage
        self.assertCanCreateAt(LinkIndexPage, LinkPage)

    def test_cant_create_under_home_page(self):
        # You can not create a LinkPage under the HomePage
        self.assertCanNotCreateAt(HomePage, LinkPage)

    def test_link_page_parent_pages(self):
        # A LinkPage can only be created under a LinkIndexPage
        self.assertAllowedParentPageTypes(LinkPage, {LinkIndexPage})
