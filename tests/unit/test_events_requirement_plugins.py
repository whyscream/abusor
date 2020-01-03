from decimal import Decimal

import pytest

from abusor.events.requirement_plugins import (
    ScoreIsAbove,
    ScoreIsBelow,
    SubjectContains,
)
from abusor.rules.plugins import RequirementPluginError

pytestmark = pytest.mark.django_db


def test_events_requirement_name():
    req = ScoreIsAbove()
    assert req.name == "ScoreIsAbove"


@pytest.mark.parametrize(
    "value, required_value, expected",
    [
        ("0", "0", False),
        ("0", "5", False),
        ("5", "0", True),
        ("5", "5", False),
        ("10", "5", True),
    ],
)
def test_events_requirement_score_is_above(
    event_factory, value, required_value, expected
):
    event = event_factory(score=Decimal(value))
    req = ScoreIsAbove()
    outcome = req(event, Decimal(required_value))
    assert outcome == expected


def test_events_requirement_score_is_above_invalid_object():
    obj = object()
    req = ScoreIsAbove()
    with pytest.raises(RequirementPluginError) as excinfo:
        req(obj, Decimal("5"))
    assert "Object of type <class 'object'> has no attribute 'score'." in str(
        excinfo.value
    )


@pytest.mark.parametrize(
    "value, required_value, expected",
    [
        ("0", "0", False),
        ("0", "5", True),
        ("5", "0", False),
        ("5", "5", False),
        ("10", "5", False),
    ],
)
def test_events_requirement_score_is_below(
    event_factory, value, required_value, expected
):
    event = event_factory(score=Decimal(value))
    req = ScoreIsBelow()
    outcome = req(event, Decimal(required_value))
    assert outcome == expected


def test_events_requirement_score_is_below_invalid_object():
    obj = object()
    req = ScoreIsBelow()
    with pytest.raises(RequirementPluginError) as excinfo:
        req(obj, Decimal("5"))
    assert "Object of type <class 'object'> has no attribute 'score'." in str(
        excinfo.value
    )


@pytest.mark.parametrize(
    "value, required_value, expected",
    [("foo", "foo", True), ("bar", "foo", False), ("FOO", "foo", True)],
)
def test_events_requirement_subject_contains(
    event_factory, value, required_value, expected
):
    event = event_factory(subject=value)
    req = SubjectContains()
    outcome = req(event, required_value)
    assert outcome == expected


def test_events_requirement_subject_contains_invalid_object():
    obj = object()
    req = SubjectContains()
    with pytest.raises(RequirementPluginError) as excinfo:
        req(obj, "foo")
    assert "Object of type <class 'object'> has no attribute 'subject'." in str(
        excinfo.value
    )
