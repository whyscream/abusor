"""Third Party and application settings."""
import sentry_sdk
from environs import Env
from sentry_sdk.integrations.django import DjangoIntegration

from ..version import VERSION
from .base import *  # noqa: F401,F403

env = Env()
env.read_env()

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "PAGE_SIZE": 10,
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
}

sentry_sdk.init(
    dsn=env("SENTRY_DSN", None),
    integrations=[DjangoIntegration()],
    send_default_pii=True,
    release=VERSION,
)

ABUSOR_SCORE_DECAY = env.float("ABUSOR_SCORE_DECAY", 0.9)
