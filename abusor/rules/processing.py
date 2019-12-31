import decimal
import logging

from .plugins import ActionProvider, PluginError, RequirementProvider

logger = logging.getLogger(__name__)

# Initialize the lists of plugins.
actions = [x() for x in ActionProvider.plugins]
requirements = [x() for x in RequirementProvider.plugins]


def str_to_any(input):
    """Convert an input string to a python native datatype.

    We try to convert the input string into:
    - an integer: "1" => 1
    - a decimal: "1.0" => Decimal("1.0")
    - or a boolean:"true" => True

    When nothing succeeds, we return the string as-is.
    """
    try:
        result = int(input)
        logger.debug(f"Converted '{input}' to int: {result}.")
        return result
    except ValueError:
        pass

    try:
        result = decimal.Decimal(input)
        logger.debug(f"Converted '{input}' to decimal: {result}.")
        return result
    except decimal.InvalidOperation:
        pass

    if input.lower() == "true":
        logger.debug(f"Converted '{input}' to boolean: True.")
        return True
    if input.lower() == "false":
        logger.debug(f"Converted '{input}' to boolean: False.")
        return False

    logger.debug(f"Returned '{input}' as string: {input}.")
    return input


def parse_kwargs_string(data):
    """Convert a string that defines kwargs into a dict.

    Example:
    the string "foo=bar, flop=2"
    will be converted into: {"foo": "bar", "flop": 2}
    """
    kwargs = {}
    if not data:
        return kwargs

    items = data.split(",")
    for item in items:
        key, value = item.strip().split("=")
        key = key.strip()
        value = str_to_any(value.strip())
        kwargs[key] = value
    return kwargs


def apply_rules(obj, rules):
    """Iterate over a queryset of rules and apply them all in order to the object."""
    num_applied = 0
    for rule in rules:
        obj, is_applied = apply_rule(obj, rule)
        if is_applied:
            num_applied += 1
    return obj, num_applied


def get_requirement(name):
    """Return a requirement by classname."""
    for requirement in requirements:
        if requirement.__class__.__name__ == name:
            return requirement


def get_action(name):
    """Return an action by classname."""
    for action in actions:
        if action.__class__.__name__ == name:
            return action


def apply_rule(obj, rule):
    """Apply a rule on an object (f.i. a Case or Event).

    We try to verify the rule requirement, and then apply the action.
    If the requirement isn't fulfilled, we don't apply the action.
    If veryfing the requirement fails, we don't apply the action.
    If applying the action fails, we return the object as-is.

    Finally, the updated object and a boolean that indicates whether the action
    was applied, is returned. The returned object isn't saved to the database.
    """
    requirement_to_apply = get_requirement(rule.requirement)
    if not requirement_to_apply:
        logger.error(f"Invalid requirement '{rule.requirement}' in rule {rule.pk}.")
        return obj, False

    try:
        param = str_to_any(rule.requirement_param)
        requirement_outcome = requirement_to_apply(obj, param)
    except PluginError as err:
        logger.error(f"Failed to verify requirement {rule.requirement} on {obj}: {err}")
        return obj, False

    if not requirement_outcome:
        logger.debug("Skipping rule {rule.pk} for case {case.pk}, requirement fails.")
        return obj, False

    action_to_apply = get_action(rule.action)
    if not action_to_apply:
        logger.error(f"Invalid action '{rule.action}' in rule {rule.pk}.")
        return obj, False

    try:
        kwargs = parse_kwargs_string(rule.action_kwargs)
        obj, result = action_to_apply(obj, **kwargs)
        if result:
            logger.info(f"Applied action {rule.action} on {obj}.")
            return obj, True
        else:
            logger.debug(f"Applied action {rule.action} on {obj} without any effect.")
            return obj, False
    except PluginError as err:
        logger.error(f"Failed to apply action {rule.action} on {obj}: {err}")
        return obj, False
