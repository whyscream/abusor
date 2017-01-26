def check_requirement(obj, when):
    """Dissect the requirement, then check whether t applies."""
    (attr, operation, search) = when

    check = REQUIREMENT_MAP[operation]
    subject = getattr(obj, attr)
    return check(subject, search)


def apply_effect(obj, effect):
    """Dissect the effect of a rule, then apply it to an object."""
    (operation, attr, value) = effect

    apply = APPLY_MAP[operation]
    return apply(obj, attr, value)


# A list of rule requirement operations
REQUIREMENT_MAP = {
    'above': lambda subject, value: float(subject) > float(value),
    'below': lambda subject, value: float(subject) < float(value),
    'contains': lambda subject, search: search.lower() in subject.lower(),
}

# A list of rule effect appliers
APPLY_MAP = {
    'call': lambda obj, attr, value: getattr(obj, attr)(value),
    'set': lambda obj, attr, value: setattr(obj, attr, value),
}
