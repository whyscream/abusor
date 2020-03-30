"""Standard Django configuration settings."""
import os.path

from environs import Env

env = Env()
env.read_env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with env.prefixed("DJANGO_"):
    SECRET_KEY = env("SECRET_KEY")
    DEBUG = env.bool("DEBUG", False)
    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", ["127.0.0.1"])
    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "abusor.events.apps.EventsConfig",
        "abusor.frontend",
        "abusor.rules.apps.RulesConfig",
        "rest_framework",
        "rest_framework.authtoken",
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
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {"format": "%(asctime)s %(name)s %(levelname)s %(message)s"}
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "console"}
        },
        "loggers": {
            "abusor": {"level": env("LOG_LEVEL", "INFO"), "handlers": ["console"]},
            "django": {"level": env("LOG_LEVEL", "INFO"), "handlers": ["console"]},
        },
    }
    WSGI_APPLICATION = "abusor.wsgi.application"
    default_database_path = os.path.join(BASE_DIR, "db.sqlite")
    DATABASES = {
        "default": env.dj_db_url("DATABASE_URL", f"sqlite:///{default_database_path}")
    }
    if "mysql" in DATABASES["default"]["ENGINE"]:
        DATABASES["default"]["ATOMIC_REQUESTS"] = True

        if "OPTIONS" not in DATABASES["default"]:
            DATABASES["default"]["OPTIONS"] = {}

        DATABASES["default"]["OPTIONS"][
            "init_command"
        ] = "SET sql_mode='STRICT_TRANS_TABLES'"

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
