import logging

from django.utils import timezone

from abusor.rules.plugins import ActionPluginError, ActionProvider

logger = logging.getLogger(__name__)


class AlterScore(ActionProvider):
    def __call__(self, obj, **kwargs):
        score = kwargs.get("score")
        if score is None:
            raise ActionPluginError("Missing required parameter 'score'.")
        self.obj_has_attribute(obj, "score")
        obj.score = obj.score + score
        return obj, True


class Close(ActionProvider):
    def __call__(self, obj, **kwargs):
        self.obj_has_attribute(obj, "end_date")
        if obj.end_date is not None:
            logger.debug(f"Object {obj} is already closed.")
            return obj, False
        obj.end_date = timezone.now()
        return obj, True


class ExpandNetworkPrefix(ActionProvider):
    def __call__(self, obj, **kwargs):
        self.obj_has_attribute(obj, "ip_network")
        self.obj_has_attribute(obj, "expand_network_prefix")

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
