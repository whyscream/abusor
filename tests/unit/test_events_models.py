from datetime import timedelta

import pytest
from django.utils import timezone

from events.models import Case, Event


pytestmark = pytest.mark.django_db

# some dates
NOW = timezone.now()
YESTERDAY = NOW - timedelta(days=1)
LAST_WEEK = NOW - timedelta(days=7)


def test_case_str_formatting(fake):
    """Verify default formatting of a Case when cast to string."""
    ipv4 = fake.ipv4()
    case = Case(ip_address=ipv4)
    result = str(case)
    assert ipv4 in result
    assert timezone.now().strftime("%Y-%m-%d") in result

    ipv6 = fake.ipv6()
    case.ip_address = ipv6
    result = str(case)
    assert ipv6 in result

    case.subject = 'foo bar'
    result = str(case)
    assert "foo bar (" + ipv6 + ")" == result


def test_event_str_formatting(fake):
    """Verify default formatting of an Event when cast to string."""
    ipv4 = fake.ipv4()
    event = Event(ip_address=ipv4, subject='foo')
    result = str(event)
    assert "foo (" + ipv4 + ")" == result

    ipv6 = fake.ipv6()
    event.ip_address = ipv6
    result = str(event)
    assert "foo (" + ipv6 + ")" == result


def test_event_find_related_case(event, case_factory):
    """Verify that we can find a related case for an event when the ip matches."""
    case = case_factory(ip_address=event.ip_address)
    result = event.find_related_case()
    assert result == case


def test_event_find_related_case_none(event, case_factory, fake):
    """Verify that finding a related Case will not work when the ip address differs."""
    case_factory(ip_address=fake.ipv4())
    result = event.find_related_case()
    assert result is None


def test_event_find_related_case_newest(event, case_factory):
    """Verify that we always find the newest Case when multiple results are available."""
    newest_case = case_factory(ip_address=event.ip_address, start_date=NOW)
    case_factory(ip_address=event.ip_address, start_date=YESTERDAY)

    result = event.find_related_case()
    assert result == newest_case


def test_event_find_related_case_opened(event, case_factory):
    """Verify that when both open and closed Cases apply to an Event, the opened one is found."""
    open_case = case_factory(ip_address=event.ip_address, end_date=None)
    case_factory(ip_address=event.ip_address, end_date=YESTERDAY)

    result = event.find_related_case()
    assert result == open_case


def test_event_find_related_case_newest_closed(event, case_factory):
    """Verify that we find the last closed Case when only closed cases apply to an Event."""
    last_closed = case_factory(ip_address=event.ip_address, end_date=YESTERDAY)
    case_factory(ip_address=event.ip_address, end_date=LAST_WEEK)

    result = event.find_related_case()
    assert result == last_closed
