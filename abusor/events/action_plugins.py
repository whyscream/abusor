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
        return obj, True


class Close(ActionProvider):
    def __call__(self, obj, **kwargs):
        if not hasattr(obj, "close"):
            type_ = type(obj)
            raise ActionPluginError(f"Object of type {type_} has no attribute 'close'.")

        result = obj.close()
        return obj, result


class ExpandNetworkPrefix(ActionProvider):
    def __call__(self, obj, **kwargs):
        if not hasattr(obj, "ip_network"):
            type_ = type(obj)
            raise ActionPluginError(
                f"Object of type {type_} has no attribute 'ip_network'."
            )

        if not hasattr(obj, "expand_network_prefix"):
            type_ = type(obj)
            raise ActionPluginError(
                f"Object of type {type_} has no attribute 'expand_network_prefix'."
            )

        if obj.ip_network.version == 4:
            prefixlen = kwargs.get("v4prefixlen")
            if prefixlen is None:
                raise ActionPluginError("Missing required parameter 'v4prefixlen'.")

        elif obj.ip_network.version == 6:
            prefixlen = kwargs.get("v6prefixlen")
            if prefixlen is None:
                raise ActionPluginError("Missing required parameter 'v6prefixlen'.")

        result = obj.expand_network_prefix(prefixlen)
        return obj, result
