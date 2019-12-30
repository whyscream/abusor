from abusor.rules.plugins import ActionPluginError, ActionProvider


class AlterScore(ActionProvider):
    def __call__(self, obj, **kwargs):
        score = kwargs.get("score")
        if score is None:
            raise ActionPluginError("Missing required parameter 'score'.")

        if not hasattr(obj, "score"):
            type_ = type(obj)
            raise ActionPluginError(f"Object of type {type_} has no attribute 'score'.")

        obj.score = obj.score + score
        return obj


class Close(ActionProvider):
    def __call__(self, obj, **kwargs):
        if not hasattr(obj, "close"):
            type_ = type(obj)
            raise ActionPluginError(f"Object of type {type_} has no attribute 'close'.")

        obj.close()
        return obj
