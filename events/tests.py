from wagtail.test.utils import WagtailPageTests

from home.models import BasicPage, HomePage

from .models import EventIndexPage, EventPage


class EventIndexPageTests(WagtailPageTests):
    def test_can_create_under_home_page(self):
        # You can create a EventIndexPage under the HomePage
        self.assertCanCreateAt(HomePage, EventIndexPage)

    def test_cant_create_under_basic_page(self):
        # You can not create a EventIndexPage under a BasicPage
        self.assertCanNotCreateAt(BasicPage, EventIndexPage)


class EventPageTests(WagtailPageTests):
    def test_can_create_under_event_index_page(self):
        # You can create a EventPage under a EventIndexPage
        self.assertCanCreateAt(EventIndexPage, EventPage)

    def test_cant_create_under_home_page(self):
        # You can not create a EventPage under the HomePage
        self.assertCanNotCreateAt(HomePage, EventPage)

    def test_event_page_parent_pages(self):
        # A EventPage can only be created under a EventIndexPage
        self.assertAllowedParentPageTypes(EventPage, {EventIndexPage})
