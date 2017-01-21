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
