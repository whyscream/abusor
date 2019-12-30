from django.apps import AppConfig

# We need to import these so the plugins are loaded.
from . import action_plugins, requirement_plugins  # noqa: F401


class EventsConfig(AppConfig):
    name = "abusor.events"
