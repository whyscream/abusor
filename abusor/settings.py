from abusor.default_settings import *

INSTALLED_APPS = INSTALLED_APPS + [
    'events',
    'rest_framework'
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'PAGE_SIZE': 10,
}
