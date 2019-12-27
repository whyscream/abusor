import ipaddress
from random import randint

import pytest

from abusor.events.models import Case, Event

pytestmark = pytest.mark.django_db


def test_new_event_creates_case(event):
    """Verify that a new Event creates a new Case."""
    assert event.case is None
    event.apply_business_rules()
    assert event.case is not None
    assert event.ip_address in str(event.case.ip_network)
    assert event.case.subject == event.subject


def test_new_event_finds_existing_case(event, case_factory):
    """Cerify that an open Case is connected to a new event when applicable."""
    case = case_factory(ip_network=ipaddress.ip_network(event.ip_address))
    assert event.case is None
    event.apply_business_rules()
    assert event.case == case
    assert (
        Case.objects.last() == case
    ), "A new case was created when it was not expected"


def test_rule_event_gets_score_assigned(event, settings, fake):
    """Verify that an event that matches the criteria gets a score assigned."""
    word = fake.word()
    score = randint(1, 999)
    settings.ABUSOR_EVENT_RULES = [
        {"when": ["subject", "contains", word], "then": ["set", "score", score]}
    ]
    event.subject = "foo {} bar".format(word)
    event.apply_business_rules()
    assert event.score == score


def test_rule_score_decay_closes_case(settings, case, event_factory):
    """Verify that when a Case score drop below a threshold, the case is closed."""
    settings.ABUSOR_CASE_RULES = [
        {"when": ["score", "below", 3], "then": ["call", "close", None]}
    ]
    event = event_factory(case=case)
    event.score = 2
    event.save()

    applied = case.apply_business_rules()
    assert applied == 1
    assert case.end_date is not None


def test_rule_applied_effects(settings, event_factory):
    """Verify the number of applied rule effects."""
    settings.ABUSOR_EVENT_RULES = [
        {"when": ["subject", "contains", "foo"], "then": ["set", "score", 5]},
        {
            "when": ["description", "contains", "bar"],
            "then": ["set", "category", Event.SPAM],
        },
    ]

    event = event_factory(subject="foo", description="bar")
    applied = event.apply_business_rules()
    assert applied == 2
