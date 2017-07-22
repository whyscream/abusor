import ipaddress
from datetime import timedelta

import pytest
from django.utils import timezone

from events.models import Case, Event

# some dates
NOW = timezone.now()
YESTERDAY = NOW - timedelta(days=1)
LAST_WEEK = NOW - timedelta(days=7)

pytestmark = pytest.mark.django_db


def test_case_str_formatting(fake):
    """Verify default formatting of a Case when cast to string."""
    ipv4 = fake.ipv4()
    case = Case(ip_network=ipv4)
    result = str(case)
    assert ipv4 in result
    assert timezone.now().strftime("%Y-%m-%d") in result

    ipv6 = fake.ipv6()
    case.ip_network = ipv6
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
    case = case_factory(ip_network=event.ip_address)
    result = event.find_related_case()
    assert result == case


def test_event_find_related_case_none(event, case_factory, fake):
    """Verify that finding a related Case will not work when the ip address differs."""
    case_factory()
    result = event.find_related_case()
    assert result is None


def test_event_find_related_case_newest(event, case_factory):
    """Verify that we always find the newest Case when multiple results are available."""
    event_network = ipaddress.ip_network(event.ip_address)
    newest_case = case_factory(ip_network=event_network, start_date=NOW)
    case_factory(ip_network=event_network, start_date=YESTERDAY)

    result = event.find_related_case()
    assert result == newest_case


def test_event_find_related_case_opened(event, case_factory):
    """Verify that when both open and closed Cases apply to an Event, the opened one is found."""
    event_network = ipaddress.ip_network(event.ip_address)
    open_case = case_factory(ip_network=event_network, start_date=LAST_WEEK, end_date=None)
    case_factory(ip_network=event_network, start_date=YESTERDAY, end_date=YESTERDAY)

    result = event.find_related_case()
    assert result == open_case


def test_event_find_related_case_closed(event, case_factory):
    """Verify that we find the no Case when only a closed cases applies to an Event."""
    event_network = ipaddress.ip_network(event.ip_address)
    case_factory(ip_network=event_network, end_date=YESTERDAY)

    result = event.find_related_case()
    assert result is None


def test_event_actual_score_decay(event_factory):
    """Verify that the actual score lowers when the Event gets older."""
    event = event_factory(score=5.0, date=NOW)
    assert event.actual_score == 5

    event.date = YESTERDAY - timedelta(hours=1)
    assert event.actual_score == 4.5

    event.date = LAST_WEEK
    assert event.actual_score == 2.39


def test_case_recalculate_score(case, event_factory):
    """Verify that the score of a Case is correctly recalculated."""
    event_factory(date=NOW, score=5, case=case)

    event = event_factory(case=case, score=5, date=NOW)
    score = case.recalculate_score()
    assert score == 10

    event.date = LAST_WEEK
    event.save()
    score = case.recalculate_score()
    assert score == 7.39

    case.close()
    score = case.recalculate_score()
    assert score is None


def test_case_expand(case_factory, event_factory):
    """Verify that cases will be merged when expanding a case in the nearby network."""
    for ip in ['192.0.2.34', '192.0.2.178', '198.51.100.17']:
        # get some test data
        case = case_factory(ip_network=ipaddress.ip_network(ip))
        event_factory(ip_address=ip, case=case)
    # generate our subject case
    case = case_factory(ip_network=ipaddress.ip_network('192.0.2.35'))
    event_factory(ip_address=ip, case=case)

    open_cases = Case.objects.filter(end_date=None)
    assert open_cases.count() == 4

    case.expand(29)
    case.save()
    case.refresh_from_db()
    assert case.events.count() == 2
    open_cases = Case.objects.filter(end_date=None)
    assert open_cases.count() == 3

    case.expand(24)
    case.save()
    case.refresh_from_db()
    assert case.events.count() == 3
    open_cases = Case.objects.filter(end_date=None)
    assert open_cases.count() == 2

    assert '192.0.2.0/24' in [str(x.ip_network) for x in open_cases]
    assert '198.51.100.17/32' in [str(x.ip_network) for x in open_cases]

    case.expand(29)
    case.save()
    case.refresh_from_db()
    assert case.ip_network.prefixlen == 24, 'prefix length was unexpectedly decreased'


def test_case_expand_ipv4(case_factory, event_factory):
    """Verify that expanding a case using the wrong protocol returns False."""
    # some fixtures
    for ip in ['192.0.2.1', '192.0.2.2']:
        case = case_factory(ip_network=ipaddress.ip_network(ip))
        event_factory(ip_address=ip, case=case)

    # subject case
    case = case_factory(ip_network=ipaddress.ip_network('192.0.2.3'))
    event_factory(ip_address='192.0.2.3', case=case)

    result = case.expand_ipv6(80)
    assert result is False
    open_cases = Case.objects.filter(end_date=None)
    assert open_cases.count() == 3
    assert case.events.count() == 1

    result = case.expand_ipv4(29)
    assert result is True
    open_cases = Case.objects.filter(end_date=None)
    assert open_cases.count() == 1
    assert case.events.count() == 3


def test_case_expand_ipv6(case_factory, event_factory):
    """Verify that expanding a case using the wrong protocol returns False."""
    # some fixtures
    for ip in ['2001:db8::1', '2001:db8::2']:
        case = case_factory(_ip_address=ip)
        event_factory(ip_address=ip, case=case)

    # subject case
    case = case_factory(ip_network=ipaddress.ip_network('2001:db8::3'))
    event_factory(ip_address='2001:db8::3', case=case)

    result = case.expand_ipv4(29)
    assert result is False
    open_cases = Case.objects.filter(end_date=None)
    assert open_cases.count() == 3
    assert case.events.count() == 1

    result = case.expand_ipv6(80)
    assert result is True
    open_cases = Case.objects.filter(end_date=None)
    assert open_cases.count() == 1
    assert case.events.count() == 3
