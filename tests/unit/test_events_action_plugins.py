import ipaddress
from decimal import Decimal

import pytest

from abusor.events.action_plugins import AlterScore, Close, ExpandNetworkPrefix
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


def test_events_action_expand_network_prefix(nearby_cases):
    case = nearby_cases[0]
    assert case.events.count() == 1
    action = ExpandNetworkPrefix()
    updated_case = action(case, v4prefixlen=29)
    assert updated_case.events.count() == 3


def test_events_action_expand_network_prefix_object_missing_ip_network_attr():
    obj = object()
    action = ExpandNetworkPrefix()
    with pytest.raises(ActionPluginError) as excinfo:
        action(obj)
    assert "Object of type <class 'object'> has no attribute 'ip_network'." in str(
        excinfo.value
    )


def test_events_action_expand_network_prefix_object_missing_expand_attr():
    class MockObject:
        ip_network = None

    obj = MockObject()
    obj.ip_network = ipaddress.IPv4Network("192.0.0.1/32")

    action = ExpandNetworkPrefix()
    with pytest.raises(ActionPluginError) as excinfo:
        action(obj)
    assert "has no attribute 'expand_network_prefix'." in str(excinfo.value)


def test_events_action_expand_network_prefix_no_kwargs(ipv4_case, ipv6_case):
    action = ExpandNetworkPrefix()
    with pytest.raises(ActionPluginError) as excinfo:
        action(ipv4_case)
    assert "Missing required parameter 'v4prefixlen'." in str(excinfo.value)

    with pytest.raises(ActionPluginError) as excinfo:
        action(ipv6_case)
    assert "Missing required parameter 'v6prefixlen'." in str(excinfo.value)


def test_events_action_expand_network_prefix_invalid_kwargs(ipv4_case, ipv6_case):
    action = ExpandNetworkPrefix()
    with pytest.raises(ActionPluginError) as excinfo:
        action(ipv4_case, foo="bar")
    assert "Missing required parameter 'v4prefixlen'." in str(excinfo.value)

    with pytest.raises(ActionPluginError) as excinfo:
        action(ipv6_case, foo="bar")
    assert "Missing required parameter 'v6prefixlen'." in str(excinfo.value)


def test_events_action_expand_network_prefix_partial_kwargs(ipv4_case, ipv6_case):
    """Verify that the action cannot succeed when the wrong kwargs are passed."""
    action = ExpandNetworkPrefix()
    with pytest.raises(ActionPluginError) as excinfo:
        action(ipv4_case, v6prefixlen=80)
    assert "Missing required parameter 'v4prefixlen'." in str(excinfo.value)

    with pytest.raises(ActionPluginError) as excinfo:
        action(ipv6_case, v4prefixlen=29)
    assert "Missing required parameter 'v6prefixlen'." in str(excinfo.value)
