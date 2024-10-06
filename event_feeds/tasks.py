import requests
from django.utils import timezone
from icalendar import Calendar

from .models import Event, EventFeed


def fetch_and_parse_feeds():
    for feed in EventFeed.objects.all():
        response = requests.get(feed.url)
        if response.status_code == 200:
            cal = Calendar.from_ical(response.text)
            for component in cal.walk():
                if component.name == "VEVENT":
                    event, created = Event.objects.update_or_create(
                        feed=feed,
                        title=component.get('summary'),
                        defaults={
                            'description': component.get('description', ''),
                            'start_date': component.get('dtstart').dt,
                            'end_date': component.get('dtend').dt if component.get('dtend') else None,
                            'location': component.get('location', ''),
                            'url': component.get('url', ''),
                        }
                    )
            feed.last_updated = timezone.now()
            feed.save()
