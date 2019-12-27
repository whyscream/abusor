import os.path

from configurations import Configuration, values

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Base(Configuration):
    """Standard Django configuration settings."""

    SECRET_KEY = values.SecretValue()
    DEBUG = values.BooleanValue(False)
    ALLOWED_HOSTS = values.ListValue([])
    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "abusor.events",
        "abusor.frontend",
        "abusor.rules",
        "rest_framework",
        "rest_framework.authtoken",
        "raven.contrib.django.raven_compat",
    ]
    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]
    ROOT_URLCONF = "abusor.urls"
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ]
            },
        }
    ]
    WSGI_APPLICATION = "abusor.wsgi.application"
    _SQLITE_DB_PATH = os.path.join(BASE_DIR, "db.sqlite")
    DATABASES = values.DatabaseURLValue(f"sqlite:///{_SQLITE_DB_PATH}")
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa: E501
        },
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]
    LANGUAGE_CODE = "en-us"
    TIME_ZONE = "UTC"
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static")


class Main(Base):
    """Third Party and application settings."""

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

    ABUSOR_SCORE_DECAY = values.FloatValue(0.9)
    ABUSOR_EVENT_RULES = []
    ABUSOR_CASE_RULES = []


class Test(Main):
    """Specific settngs for test runs."""

    SECRET_KEY = "secret"
