from decimal import Decimal

import pytest

from abusor.events.action_plugins import AlterScore, Close
from abusor.rules.plugins import ActionPluginError

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "value, action_value, expected",
    [("0", "5", "5"), ("1", "5", "6"), ("5", "-1", "4")],
)
def test_events_action_alter_score(event_factory, value, action_value, expected):
    event = event_factory(score=Decimal(value))
    action = AlterScore()
    updated_event = action(event, score=Decimal(action_value))
    assert updated_event.score == Decimal(expected)


def test_events_action_alter_score_no_kwargs():
    obj = object()
    action = AlterScore()
    with pytest.raises(ActionPluginError) as excinfo:
        action(obj)  # no kwargs
    assert "Missing required parameter 'score'." in str(excinfo.value)


def test_events_action_alter_score_invalid_kwargs():
    obj = object()
    action = AlterScore()
    with pytest.raises(ActionPluginError) as excinfo:
        action(obj, foo="bar")
    assert "Missing required parameter 'score'." in str(excinfo.value)


def test_events_action_alter_score_invalid_object():
    obj = object()
    action = AlterScore()
    with pytest.raises(ActionPluginError) as excinfo:
        action(obj, score=Decimal("5"))
    assert "Object of type <class 'object'> has no attribute 'score'." in str(
        excinfo.value
    )


def test_events_action_close(case):
    assert case.end_date is None
    action = Close()
    updated_case = action(case)
    assert updated_case.end_date is not None


def test_events_action_close_invalid_object():
    obj = object()
    action = Close()
    with pytest.raises(ActionPluginError) as excinfo:
        action(obj)
    assert "Object of type <class 'object'> has no attribute 'close'." in str(
        excinfo.value
    )
