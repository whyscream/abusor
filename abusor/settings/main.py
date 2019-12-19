from abusor.settings.django import *  # noqa

INSTALLED_APPS = INSTALLED_APPS + [
    'abusor',
    'abusor.events',
    'rest_framework',
    'rest_framework.authtoken',
    'raven.contrib.django.raven_compat',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
}

ABUSOR_SCORE_DECAY = 0.9
ABUSOR_EVENT_RULES = []
ABUSOR_CASE_RULES = []

try:
    # load custom settings when available
    from abusor.settings.custom import *  # noqa
except ImportError:
    pass
