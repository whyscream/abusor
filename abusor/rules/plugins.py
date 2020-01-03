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


class PluginBase:
    @property
    def name(self):
        """Render a short name for the plugin."""
        return self.__class__.__name__


class RequirementProvider(PluginBase, metaclass=PluginMount):
    @staticmethod
    def obj_has_attribute(obj, attr):
        """Validate the existence of an attribute, raise an error when it's missing."""
        if not hasattr(obj, attr):
            type_ = type(obj)
            raise RequirementPluginError(
                f"Object of type {type_} has no attribute '{attr}'."
            )


class ActionProvider(PluginBase, metaclass=PluginMount):
    @staticmethod
    def obj_has_attribute(obj, attr):
        """Validate the existence of an attribute, raise an error when it's missing."""
        if not hasattr(obj, attr):
            type_ = type(obj)
            raise ActionPluginError(
                f"Object of type {type_} has no attribute '{attr}'."
            )


class PluginError(Exception):
    pass


class ActionPluginError(PluginError):
    pass


class RequirementPluginError(PluginError):
    pass
