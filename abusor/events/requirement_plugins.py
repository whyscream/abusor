from abusor.rules.plugins import RequirementProvider


class ScoreIsAbove(RequirementProvider):
    def __call__(self, obj, value):
        self.obj_has_attribute(obj, "score")
        return obj.score > value


class ScoreIsBelow(RequirementProvider):
    def __call__(self, obj, value):
        self.obj_has_attribute(obj, "score")
        return obj.score < value


class SubjectContains(RequirementProvider):
    def __call__(self, obj, value):
        self.obj_has_attribute(obj, "subject")
        return value.lower() in obj.subject.lower()
