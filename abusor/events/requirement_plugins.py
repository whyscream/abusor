from abusor.rules.plugins import RequirementPluginError, RequirementProvider


class ScoreIsAbove(RequirementProvider):
    def __call__(self, obj, value):
        if not hasattr(obj, "score"):
            type_ = type(obj)
            raise RequirementPluginError(
                f"Object with type {type_} has no attribute 'score'."
            )
        return obj.score > value


class ScoreIsBelow(RequirementProvider):
    def __call__(self, obj, value):
        if not hasattr(obj, "score"):
            type_ = type(obj)
            raise RequirementPluginError(
                f"Object with type {type_} has no attribute 'score'."
            )
        return obj.score < value


class SubjectContains(RequirementProvider):
    def __call__(self, obj, value):
        if not hasattr(obj, "subject"):
            type_ = type(obj)
            raise RequirementPluginError(
                f"Object with type {type_} has no attribute 'subject'."
            )
        return value.lower() in obj.subject.lower()
