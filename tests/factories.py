from datetime import timedelta

import factory
import factory.fuzzy
from django.utils import timezone

from events.models import Case, Event

# some convenient dates
NOW = timezone.now()
LAST_YEAR = NOW - timedelta(days=365)


class EventFactory(factory.DjangoModelFactory):

    class Meta:
        model = Event

    ip_address = factory.Faker('ipv4')
    date = factory.fuzzy.FuzzyDateTime(LAST_YEAR)
    subject = factory.Faker('sentence')


class CaseFactory(factory.DjangoModelFactory):

    class Meta:
        model = Case

    ip_address = factory.Faker('ipv4')

    @factory.post_generation
    def related_event(self, create, extracted, **kwargs):
        """Create a related Event for the Case."""
        EventFactory.simple_generate(
            create=create, case=self, ip_address=self.ip_address,
            date=self.start_date)
