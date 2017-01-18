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
