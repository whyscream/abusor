import ipaddress
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
    existing_event = case.events.first()
    existing_event.date = NOW
    existing_event.score = 5
    existing_event.save()

    event = event_factory(case=case, score=5, date=NOW)
    score = case.recalculate_score()
    assert score == 10

    event.date = LAST_WEEK
    event.save()
    score = case.recalculate_score()
    assert score == 7.39


@pytest.mark.parametrize('ip, netmask, expected', [
    ('192.0.2.34', None, '192.0.2.34/32'),
    ('192.0.2.34', 32, '192.0.2.34/32'),
    ('192.0.2.34', 29, '192.0.2.32/29'),
    ('192.0.2.34', 24, '192.0.2.0/24'),
    ('192.0.2.34', 16, '192.0.0.0/16'),
    ('192.0.2.34', 13, '192.0.0.0/13'),
    ('2001:db8:7ff5:9ee4:f49e:27cb:bd6e:936d', None, '2001:db8:7ff5:9ee4:f49e:27cb:bd6e:936d/128'),
    ('2001:db8:7ff5:9ee4:f49e:27cb:bd6e:936d', 128, '2001:db8:7ff5:9ee4:f49e:27cb:bd6e:936d/128'),
    ('2001:db8:7ff5:9ee4:f49e:27cb:bd6e:936d', 80, '2001:db8:7ff5:9ee4:f49e::/80'),
    ('2001:db8:7ff5:9ee4:f49e:27cb:bd6e:936d', 64, '2001:db8:7ff5:9ee4::/64'),
    ('2001:db8:7ff5:9ee4:f49e:27cb:bd6e:936d', 32, '2001:db8::/32'),
])
def test_case_get_ip_network(case_factory, ip, netmask, expected):
    """Verify that ip_network is correcty reported."""
    case = case_factory.build(ip_address=ip, netmask=netmask)
    assert case.ip_network == ipaddress.ip_network(expected)


def test_case_expand(case_factory):
    """Vreify that cases will be merged when expanding a case in the nearby network."""
    for ip in ['192.0.2.34', '192.0.2.178', '198.51.100.17']:
        case_factory(ip_address=ip)
    case = case_factory(ip_address='192.0.2.35')

    open_cases = Case.objects.filter(end_date=None)
    assert open_cases.count() == 4

    case.expand(29)
    case.refresh_from_db()
    assert case.events.count() == 2
    open_cases = Case.objects.filter(end_date=None)
    assert open_cases.count() == 3

    case.expand(24)
    case.refresh_from_db()
    assert case.events.count() == 3
    open_cases = Case.objects.filter(end_date=None)
    assert open_cases.count() == 2

    assert '192.0.2.35' in [x.ip_address for x in open_cases]
    assert '198.51.100.17' in [x.ip_address for x in open_cases]
