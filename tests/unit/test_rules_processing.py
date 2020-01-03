from decimal import Decimal
from ipaddress import ip_network

import pytest

from abusor.rules.models import CaseRule, EventRule
from abusor.rules.processing import apply_rules, parse_kwargs_string, str_to_any

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "input, expected",
    [
        ("", {}),
        ("foo=bar", {"foo": "bar"}),
        ("foo=bar,brol=flop", {"foo": "bar", "brol": "flop"}),
        ("foo=2", {"foo": 2}),
        ("foo=2.0", {"foo": Decimal("2.0")}),
        ("foo=true,bar=false", {"foo": True, "bar": False}),
        ("with=spaces, in=between", {"with": "spaces", "in": "between"}),
    ],
)
def test_parse_kwargs_string(input, expected):
    result = parse_kwargs_string(input)
    assert result == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        ("1", 1),
        ("-1", -1),
        ("1.0", Decimal("1.0")),
        ("-1.0", Decimal("-1.0")),
        ("true", True),
        ("FALSE", False),
        ("hoeba", "hoeba"),
    ],
)
def test_str_to_any(input, expected):
    result = str_to_any(input)
    assert result == expected


def test_eventrule_apply(event_factory):
    EventRule.objects.create(
        requirement="SubjectContains",
        requirement_param="foo",
        action="AlterScore",
        action_kwargs="score=5",
    )
    event = event_factory(subject="this contains foo")
    assert event.score == Decimal("0.0")

    updated_event, num_applied = apply_rules(event, EventRule.objects.all())
    assert num_applied == 1
    assert updated_event.score == Decimal("5")


def test_eventrule_apply_invalid_requirement(event, caplog):
    rule = EventRule.objects.create(
        requirement="DoesNotExist",
        requirement_param="foo",
        action="AlterScore",
        action_kwargs="score=5",
    )
    updated_event, num_applied = apply_rules(event, EventRule.objects.all())
    assert num_applied == 0

    assert (
        f"Error while processing rule {rule}: "
        f"Requirement 'DoesNotExist' does not exist." in caplog.text
    )


def test_rule_apply_invalid_object(caplog):
    EventRule.objects.create(
        requirement="SubjectContains",
        requirement_param="foo",
        action="AlterScore",
        action_kwargs="score=5",
    )
    obj = object()

    updated_obj, num_applied = apply_rules(obj, EventRule.objects.all())
    assert num_applied == 0

    assert (
        "Failed to verify requirement SubjectContains: Object of type <class 'object'> "
        "has no attribute 'subject'." in caplog.text
    )


def test_eventrule_apply_requirement_does_not_fulfill(event_factory):
    event = event_factory(subject="bar")
    EventRule.objects.create(
        requirement="SubjectContains",
        requirement_param="foo",
        action="AlterScore",
        action_kwargs="score=5",
    )
    assert event.score == Decimal("0.0")

    updated_event, num_applied = apply_rules(event, EventRule.objects.all())
    assert num_applied == 0
    assert updated_event.score == Decimal("0")


def test_eventrule_apply_invalid_action(event_factory, caplog):
    EventRule.objects.create(
        requirement="SubjectContains",
        requirement_param="foo",
        action="DoesNotExist",
        action_kwargs="score=5",
    )
    event = event_factory(subject="this contains foo")

    updated_event, num_applied = apply_rules(event, EventRule.objects.all())
    assert num_applied == 0

    assert "Invalid action 'DoesNotExist' in rule" in caplog.text


def test_eventrule_apply_action_failed(event_factory, caplog):
    EventRule.objects.create(
        requirement="SubjectContains",
        requirement_param="foo",
        action="AlterScore",
        action_kwargs="invalid=kwargs",
    )
    event = event_factory(subject="this contains foo")

    updated_event, num_applied = apply_rules(event, EventRule.objects.all())
    assert num_applied == 0

    assert "Failed to apply action AlterScore on <Event" in caplog.text
    assert "Missing required parameter 'score'." in caplog.text


def test_eventrule_applied_action_no_effect(case_factory, caplog):
    CaseRule.objects.create(
        requirement="SubjectContains",
        requirement_param="foo",
        action="ExpandNetworkPrefix",
        action_kwargs="v4prefixlen=32",
    )
    case = case_factory(
        ip_network=ip_network("192.0.0.1/32"), subject="this contains foo"
    )

    updated_case, num_applied = apply_rules(case, CaseRule.objects.all())
    assert num_applied == 0
    assert case.ip_network == ip_network("192.0.0.1/32"), "Prefixlength was changed."
