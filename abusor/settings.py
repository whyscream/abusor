from abusor.default_settings import *  # noqa

INSTALLED_APPS = INSTALLED_APPS + [
    'abusor',
    'events',
    'rest_framework',
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'PAGE_SIZE': 10,
}

ABUSOR_EVENT_RULES = []
ABUSOR_CASE_RULES = []

try:
    # load custom settings when available
    from abusor.custom_settings import *  # noqa
except ImportError:
    pass
