from django.core.management.base import BaseCommand

from events.models import Event


class Command(BaseCommand):
    help = "Handle previously unprocessed events."

    def handle(self, *args, **kwargs):
        """Find events without an attached case, and fix that."""
        events = Event.objects.filter(case=None)
        if not events:
            self.stdout.write(self.style.SUCCESS('No unprocessed events found.'))
            return

        for event in events:
            event.save()
        self.stdout.write(self.style.SUCCESS('Processed {} events.'.format(events.count())))
