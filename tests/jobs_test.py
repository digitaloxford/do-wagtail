# from wagtail.test.utils import WagtailPageTestCase

# from home.models import BasicPage, HomePage
# from jobs.models import JobIndexPage, JobPage, RecruiterPage


# class JobIndexPageTests(WagtailPageTestCase):
#     def test_can_create_under_home_page(self):
#         # You can create a JobIndexPage under the HomePage
#         self.assertCanCreateAt(HomePage, JobIndexPage)

#     def test_cant_create_under_basic_page(self):
#         # You can not create a JobIndexPage under a BasicPage
#         self.assertCanNotCreateAt(BasicPage, JobIndexPage)


# class RecruiterPageTests(WagtailPageTestCase):
#     def test_can_create_under_job_index_page(self):
#         # You can create a RecruiterPage under a JobIndexPage
#         self.assertCanCreateAt(JobIndexPage, RecruiterPage)

#     def test_cant_create_under_home_page(self):
#         # You can not create a RecruiterPage under the HomePage
#         self.assertCanNotCreateAt(HomePage, RecruiterPage)

#     def test_job_page_parent_pages(self):
#         # A RecruiterPage can only be created under a JobIndexPage
#         self.assertAllowedParentPageTypes(RecruiterPage, {JobIndexPage})


# class JobPageTests(WagtailPageTestCase):
#     def test_can_create_under_recruiter_page(self):
#         # You can create a JobPage under a RecruiterPage
#         self.assertCanCreateAt(RecruiterPage, JobPage)

#     def test_job_page_parent_pages(self):
#         # A JobPage can only be created under a RecruiterPage
#         self.assertAllowedParentPageTypes(JobPage, {RecruiterPage})

#     def test_cant_create_under_home_page(self):
#         # You can not create a JobPage under the HomePage
#         self.assertCanNotCreateAt(HomePage, JobPage)

#     def test_cant_create_under_job_index_page(self):
#         # You can not create a JobPage under the JobIndexPage
#         self.assertCanNotCreateAt(JobIndexPage, JobPage)
