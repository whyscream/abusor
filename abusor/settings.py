import os.path
from configurations import Configuration


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Base(Configuration):
	"""Standard Django configuration settings."""
	SECRET_KEY = ')59*k1_78ylzrqza0#l%!2yr2%-e)r1dc6j*6i3bezt^3(jfnh'
	DEBUG = True
	ALLOWED_HOSTS = []
	INSTALLED_APPS = [
	    'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.messages',
	    'django.contrib.staticfiles',
	    'abusor',
	    'abusor.events',
	    'abusor.frontend',
	    'rest_framework',
	    'rest_framework.authtoken',
	    'raven.contrib.django.raven_compat',
	]
	MIDDLEWARE = [
	    'django.middleware.security.SecurityMiddleware',
	    'django.contrib.sessions.middleware.SessionMiddleware',
	    'django.middleware.common.CommonMiddleware',
	    'django.middleware.csrf.CsrfViewMiddleware',
	    'django.contrib.auth.middleware.AuthenticationMiddleware',
	    'django.contrib.messages.middleware.MessageMiddleware',
	    'django.middleware.clickjacking.XFrameOptionsMiddleware',
	]
	ROOT_URLCONF = 'abusor.urls'
	TEMPLATES = [
	    {
	        'BACKEND': 'django.template.backends.django.DjangoTemplates',
	        'DIRS': [],
	        'APP_DIRS': True,
	        'OPTIONS': {
	            'context_processors': [
	                'django.template.context_processors.debug',
	                'django.template.context_processors.request',
	                'django.contrib.auth.context_processors.auth',
	                'django.contrib.messages.context_processors.messages',
	            ],
	        },
	    },
	]
	WSGI_APPLICATION = 'abusor.wsgi.application'
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.sqlite3',
	        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	    }
	}
	AUTH_PASSWORD_VALIDATORS = [
	    {
	        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	    },
	    {
	        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	    },
	    {
	        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	    },
	    {
	        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	    },
	]
	LANGUAGE_CODE = 'en-us'
	TIME_ZONE = 'UTC'
	USE_I18N = True
	USE_L10N = True
	USE_TZ = True
	STATIC_URL = '/static/'
	STATIC_ROOT = os.path.join(BASE_DIR, "static")


class Main(Base):
    """Third Party and application settings."""
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
