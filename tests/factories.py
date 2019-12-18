import ipaddress
from datetime import timedelta

import factory
import factory.fuzzy
from django.utils import timezone

from abusor.events.models import Case, Event

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
        exclude = ('_ip_address', '_netmask')

    _ip_address = factory.Faker('ipv4')
    _netmask = factory.fuzzy.FuzzyInteger(13, 32)
    ip_network = factory.LazyAttribute(
        lambda obj: ipaddress.ip_network('{0._ip_address}/{0._netmask}'.format(obj), strict=False))
