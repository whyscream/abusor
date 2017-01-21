from random import randint

import pytest

from events.models import Case


pytestmark = pytest.mark.django_db


def test_new_event_creates_case(event):
    """Verify that a new Event creates a new Case."""
    assert event.case is None
    event.apply_business_rules()
    assert event.case is not None
    assert event.case.ip_address == event.ip_address
    assert event.case.subject == event.subject


def test_new_event_finds_existing_case(case, event_factory):
    """Cerify that an open Case is connected to a new event when applicable."""
    event = event_factory(ip_address=case.ip_address)
    assert event.case is None
    event.apply_business_rules()
    assert event.case == case
    assert Case.objects.last() == case, "A new case was created when it was not expected"


def test_rule_event_gets_score_assigned(event, settings, fake):
    """Verify that an event that matches the criteria gets a score assigned."""
    word = fake.word()
    score = randint(1, 999)
    settings.ABUSOR_EVENT_RULES = [{
        'when': ['subject', 'contains', word],
        'then': ['set', 'score', score]
    }]
    event.subject = 'foo {} bar'.format(word)
    event.apply_business_rules()
    assert event.score == score


def test_rule_score_decay_closes_case(settings, case):
    """Verify that when a Case score drop below a threshold, the case is closed."""
    settings.ABUSOR_CASE_RULES = [{
        'when': ['score', 'below', 3],
        'then': ['call', 'close', None]
    }]
    event = case.events.first()
    event.score = 2
    event.save()

    case.apply_business_rules()
    assert case.end_date is not None
