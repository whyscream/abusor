import pytest
from django.utils import timezone

from events.models import Event


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
    event = Event.objects.create(ip_address=random_ipv4, date=timezone.now(), subject='foo')
    assert event.case is not None
    assert event.case.ip_address == random_ipv4
    assert event.case.subject == 'foo'
