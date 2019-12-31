"""Plugin system based on http://martyalchin.com/2008/jan/10/simple-plugin-framework/"""
import logging

logger = logging.getLogger(__name__)


class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, "plugins"):
            logger.debug(f"Initialized plugin registry for {name}.")
            cls.plugins = []
        else:
            # find out plugin parent
            parent = None
            for klass in bases:
                if klass.__module__ == "abusor.rules.plugins":
                    parent = klass.__name__
                    break
            logger.debug(f"Registered plugin {name} to {parent}.")
            cls.plugins.append(cls)


class RequirementProvider(object, metaclass=PluginMount):
    pass


class ActionProvider(object, metaclass=PluginMount):
    pass


class PluginError(Exception):
    pass


class ActionPluginError(PluginError):
    pass


class RequirementPluginError(PluginError):
    pass
