from decimal import Decimal

from abusor.rules.plugins import RequirementPluginError, RequirementProvider


class ScoreIsAbove(RequirementProvider):
    def __call__(self, obj, value):
        if not isinstance(value, Decimal):
            raise RequirementPluginError(f"Value '{value}' is no decimal.")
        self.obj_has_attribute(obj, "score")
        return obj.score > value


class ScoreIsBelow(RequirementProvider):
    def __call__(self, obj, value):
        if not isinstance(value, Decimal):
            raise RequirementPluginError(f"Value '{value}' is no decimal.")
        self.obj_has_attribute(obj, "score")
        return obj.score < value


class SubjectContains(RequirementProvider):
    def __call__(self, obj, value):
        if not isinstance(value, str):
            raise RequirementPluginError(f"Value '{value}' is no string.")
        self.obj_has_attribute(obj, "subject")
        return value.lower() in obj.subject.lower()
