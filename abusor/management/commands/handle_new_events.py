from django.core.management.base import BaseCommand

from events.models import Event
from events.utils import find_as_number


class Command(BaseCommand):
    help = "Handle new events."

    def handle(self, *args, **kwargs):
        """Find events without an attached case, and  apply business rules to them."""
        events = Event.objects.filter(case=None)
        if not events:
            self.stdout.write(self.style.SUCCESS('No new events found.'))
            return

        for event in events:
            if not event.as_number:
                event.as_number = find_as_number(event.ip_address)
            event.apply_business_rules()
            if event.case:
                event.case.apply_business_rules()
        self.stdout.write(self.style.SUCCESS('Processed {} new events.'.format(events.count())))
