from datetime import timedelta

import pytest
from django.utils import timezone

from events.utils import find_related_case


pytestmark = pytest.mark.django_db

# some dates
NOW = timezone.now()
YESTERDAY = NOW - timedelta(days=1)
LAST_WEEK = NOW - timedelta(days=7)


def test_find_related_case(event, case_factory):
    """Verify that we can find a related case for an event when the ip matches."""
    case = case_factory(ip_address=event.ip_address)
    result = find_related_case(event)
    assert result == case


def test_find_related_case_none(event, case_factory, random_ipv6):
    """Verify that finding a related case will not work when the ip address differs."""
    case_factory(ip_address=random_ipv6)
    result = find_related_case(event)
    assert result is None


def test_find_related_case_newest(event, case_factory):
    """Verify that we always find the newest case when multiple results are available."""
    case1 = case_factory(ip_address=event.ip_address, start_date=YESTERDAY)
    case2 = case_factory(ip_address=event.ip_address, start_date=NOW)

    result = find_related_case(event)
    assert result != case1
    assert result == case2
