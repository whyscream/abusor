import ipaddress

from django.core.management.base import BaseCommand

from abusor.events.models import Event
from abusor.events.utils import find_as_number, find_country_code
from abusor.rules.models import CaseRules, EventRules
from abusor.rules.processing import apply_rules


class Command(BaseCommand):
    help = "Handle new events."

    def handle(self, *args, **kwargs):
        """Find events without an attached case, and  apply business rules to them."""
        events = Event.objects.filter(case=None)
        if not events:
            self.stdout.write(self.style.SUCCESS("No new events found."))
            return

        for event in events:
            event_updated = False
            if not event.as_number or not event.country_code:
                # cast to IPv4Address/IPv6Address object
                ip_address = ipaddress.ip_address(event.ip_address)
                if not event.as_number:
                    event.as_number = find_as_number(ip_address) or -1
                if not event.country_code:
                    event.country_code = find_country_code(ip_address) or "--"
                event_updated = True

            event, num_applied = apply_rules(event, EventRules.objects.all())
            if event_updated or num_applied:
                event.save()

            case = event.get_or_create_case()
            case, num_applied = apply_rules(case, CaseRules.objects.all())
            if num_applied:
                case.save()
        self.stdout.write(self.style.SUCCESS(f"Processed {events.count()} new events."))
