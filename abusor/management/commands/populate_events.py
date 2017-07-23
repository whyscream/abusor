import ipaddress

from django.core.management.base import BaseCommand
from django.db.models import Q

from events.models import Event
from events.utils import find_as_number, find_country_code


class Command(BaseCommand):
    help = 'Populate existing Events with additional data from third-party sources'

    def handle(self, *args, **kwargs):
        """Populate events with third-party data."""
        events = Event.objects.filter(
            Q(as_number__isnull=True) |
            Q(country_code='')
        )
        self.stdout.write('Examining {} events.'.format(len(events)))

        updates = 0
        for event in events:
            updated = False
            ip_address = ipaddress.ip_address(event.ip_address)
            if not event.as_number:
                event.as_number = find_as_number(ip_address) or -1
                updated = True
            if not event.country_code:
                event.country_code = find_country_code(ip_address) or '--'
                updated = True
            if updated:
                updates += 1
                event.save()
        self.stdout.write(self.style.SUCCESS('Updated {} events with new data.'.format(updates)))
