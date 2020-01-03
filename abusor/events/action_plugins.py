import logging
from decimal import Decimal

from django.utils import timezone

from abusor.rules.plugins import ActionPluginError, ActionProvider

logger = logging.getLogger(__name__)


class AlterScore(ActionProvider):
    def __call__(self, obj, **kwargs):
        score = kwargs.get("score")
        if score is None:
            raise ActionPluginError("Missing required parameter 'score'.")
        if not isinstance(score, Decimal):
            raise ActionPluginError(f"Value '{score}' for score is no decimal.")

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
            if not isinstance(prefixlen, int):
                raise ActionPluginError(
                    f"Value '{prefixlen} for v4prefixlen is no integer."
                )

        elif obj.ip_network.version == 6:
            prefixlen = kwargs.get("v6prefixlen")
            if prefixlen is None:
                raise ActionPluginError("Missing required parameter 'v6prefixlen'.")
            if not isinstance(prefixlen, int):
                raise ActionPluginError(
                    f"Value '{prefixlen}' for v6prefixlen is no integer."
                )

        result = obj.expand_network_prefix(prefixlen)
        return obj, result
