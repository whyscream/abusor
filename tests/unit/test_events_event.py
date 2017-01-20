import pytest
from django.utils import timezone

from events.models import Case, Event


NOW = timezone.now()


def test_event_str_formatting(random_ipv4, random_ipv6):
    """Verify default formatting of an Event when cast to string."""
    event = Event(ip_address=random_ipv4, subject='foo')
    result = str(event)
    assert "foo (" + random_ipv4 + ")" == result

    event.ip_address = random_ipv6
    result = str(event)
    assert "foo (" + random_ipv6 + ")" == result


@pytest.mark.django_db
def test_create_event_creates_case(random_ipv4):
    """Verify that a new Event also creates a new Case."""
    event = Event.objects.create(ip_address=random_ipv4, date=NOW, subject='foo')
    assert event.case is not None
    assert event.case.ip_address == random_ipv4
    assert event.case.subject == 'foo'


@pytest.mark.django_db
def test_create_event_finds_existing_case(case):
    """Cerify that an open Case is connected to a new event when applicable."""
    event = Event.objects.create(ip_address=case.ip_address, date=NOW, subject='foo')
    assert event.case == case
    assert Case.objects.last() == case, "A new case was created when it was not expected"
