from allauth.account.signals import email_confirmed
from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from wagtail.models import Group, GroupPagePermission
from wagtail.users.models import UserProfile

from users.models import User

from .models import JobIndexPage, RecruiterPage


@receiver(email_confirmed)
def group_and_profiles(request, email_address, **kwargs):
    """Add new user to their own group, create wagtail and user profile fields with a default language setting, then create profile page and assign permissions."""

    current_site = get_current_site(request)
    user = User.objects.get(email=email_address)

    if user.is_anonymous:
        pass
    else:
        # Create a group object that matches their username
        new_group, created = Group.objects.get_or_create(name=user.username)
        user.groups.add(new_group)

        # Create new permission to access wagtail admin and set account to inactive for
        # admin approval
        access_admin = Permission.objects.get(codename="access_admin")
        new_group.permissions.add(access_admin)
        user.is_active = False
        user.save()

        # Create Wagtail and custom user profile
        wagtail_userprofile_defaults = {
            "submitted_notifications": False,
            "approved_notifications": False,
            "rejected_notifications": False,
            "preferred_language": "en",
        }
        custom_userprofile_defaults = {
            "display_name": user.id,
        }
        UserProfile.objects.get_or_create(
            user_id=user.id, defaults=wagtail_userprofile_defaults
        )
        User.objects.get_or_create(id=user.id, defaults=custom_userprofile_defaults)

        # Create recruiters page and add group permissions
        jobs_index_page = JobIndexPage.objects.filter(title="Jobs").get()
        recruiter_page = RecruiterPage(
            user=user,
            title=user.display_name,
            draft_title=user.display_name,
            owner_id=user.id,
            show_in_menus=False,
        )

        # Save as a child of the Jobs index page and submit for moderation
        recruiter = jobs_index_page.add_child(instance=recruiter_page)

        if recruiter:
            recruiter.unpublish()

            # Submit page for moderation. This requires first saving a revision.
            recruiter.save_revision(user=user, submitted_for_moderation=True)

            # Notify administrator
            ADMIN_EMAIL_SUBJECT = "[{site_name}] A new recruiter has signed up".format(
                site_name=current_site.name
            )
            ADMIN_EMAIL_MESSAGE = """A new recruiter {first_name} {last_name} ({email}) has signed up on {site_name}. Best check them out.""".format(
                site_name=current_site.name,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
            )
            ADMIN_EMAIL_FROM = settings.WAGTAILADMIN_NOTIFICATION_FROM_EMAIL
            ADMIN_EMAIL_TO = [settings.WAGTAILADMIN_NOTIFICATION_FROM_EMAIL]

            send_mail(
                ADMIN_EMAIL_SUBJECT,
                ADMIN_EMAIL_MESSAGE,
                ADMIN_EMAIL_FROM,
                ADMIN_EMAIL_TO,
                fail_silently=False,
            )

            # Notify user
            USER_EMAIL_SUBJECT = (
                "[{site_name}] Thank you for confirming your email address".format(
                    site_name=current_site.name
                )
            )
            USER_EMAIL_MESSAGE = """
Hello,

Thank you for confirming that {email} is indeed a real address.

A {site_name} administrator will shortly look over your details and if all is well they will approve your account. This usually doesn't take too long, and you'll be notified by email when it's done.

Regards

{site_name}
            """.format(
                site_name=current_site.name, email=user.email
            )
            USER_EMAIL_FROM = settings.WAGTAILADMIN_NOTIFICATION_FROM_EMAIL
            USER_EMAIL_TO = [user.email]

            send_mail(
                USER_EMAIL_SUBJECT,
                USER_EMAIL_MESSAGE,
                USER_EMAIL_FROM,
                USER_EMAIL_TO,
                fail_silently=False,
            )

        # Add page to user specific permissions group
        GroupPagePermission.objects.create(
            group=new_group, page=recruiter_page, permission_type="add"
        )


@receiver(pre_save, sender=User)
def publish_profile(sender, instance, *args, **kwargs):
    """Publish Recruitment page when marking user account active and notify the user."""

    current_site = get_current_site(request=None)

    try:
        previous = User.objects.get(id=instance.id)
    except User.DoesNotExist:
        previous = None

    if previous:
        if instance.is_active and previous.is_active is False:

            recruiter = RecruiterPage.objects.get(user_id=instance.id)

            if recruiter:
                recruiter.save_revision().publish()

                # send email
                EMAIL_SUBJECT = (
                    "[{site_name}] Your recruitment profile is now live".format(
                        site_name=current_site.name
                    )
                )
                EMAIL_MESSAGE = """
Hello,

Your recruitment page for {name} ({email}) is now live on {site_name}.

You can go ahead and log in, update your profile, and start posting jobs: https://{site_domain}/accounts/login

Note: Job postings will go into a moderation queue before publication.

Regards

{site_name}
                """.format(
                    site_name=current_site.name,
                    site_domain=current_site.domain,
                    name=instance.display_name,
                    email=instance.email,
                )
                EMAIL_FROM = settings.WAGTAILADMIN_NOTIFICATION_FROM_EMAIL
                EMAIL_TO = [instance.email]

                send_mail(
                    EMAIL_SUBJECT,
                    EMAIL_MESSAGE,
                    EMAIL_FROM,
                    EMAIL_TO,
                    fail_silently=False,
                )


# @receiver(pre_save, sender=User)
# def unpublish_profile(sender, instance, *args, **kwargs):
#     """Unpublish Recruitment page when marking user account inactive."""
#     if instance.id != None:
#         previous = User.objects.get(id=instance.id)

#         if previous:
#             if instance.is_active is False and previous.is_active:
#                 # Get recruitment page
#                 recruiter = RecruiterPage.objects.get(user_id=instance.id)

#                 if recruiter:
#                     recruiter.unpublish()
