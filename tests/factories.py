from datetime import timedelta

import factory
import factory.fuzzy
from django.utils import timezone

from events.models import Event

# some convenient dates
NOW = timezone.now()
LAST_YEAR = NOW - timedelta(days=365)


class EventFactory(factory.DjangoModelFactory):

    class Meta:
        model = Event

    ip_address = factory.Faker('ipv4')
    date = factory.fuzzy.FuzzyDateTime(LAST_YEAR)
    subject = factory.Faker('sentence')
