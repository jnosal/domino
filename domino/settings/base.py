import os


here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
root = lambda *x: here('..', '..', *x)

SECRET_KEY = '*#($erce@=12731628768%8mph$7iag8gn$#&tw43a35b5wj'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']
SITE_ID = 1
PROJECT_NAME = 'Domino'

BASE_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sites',
)

THIRD_PARTY_APPS = (
    'rest_framework',
)

LOCAL_APPS = (
    'apps.core',
    'apps.colors',
)


INSTALLED_APPS = BASE_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.DummyBackend',
    }
}


ROOT_URLCONF = 'domino.urls'
WSGI_APPLICATION = 'domino.wsgi.application'


APP_ROOT = root()
LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = root('statics_collected')
MEDIA_ROOT = root('media')

TEMPLATE_DIRS = (
    root('templates'),
)

STATICFILES_DIRS = (
    root('static'),
)

FILE_UPLOAD_HANDLERS = (
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
)

# image content types that are considered valid
IMAGE_CONTENT_TYPES = [
    'image/jpeg', 'image/pipeg'
]

# whether to handle color extraction syncrhonously or asynchronously
# available options 'async' or 'sync'
IMAGE_EXTRACTION_MODE = 'async'

# 2 options available all, hex, name.
# if name - unique set of colors based on name will be saved
# if hex - unique set of colors based on hex will be saved
# Since names are somewhat estimated for instace triplets (255, 255, 255), (252, 255, 255)
# may be represented by same color name

IMAGE_COLOR_PERSIST_MODE = 'name'

# size of pallette of colors extracted from image
IMAGE_VITAL_COLORS_COUNT = 5


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50
}


BROKER_URL = 'amqp://guest:guest@localhost:5672//'


import sys

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            # 'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'app.location': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'domino': {
            'handlers': ['console'],
            'level': 'INFO',
            'filters': []
        }
    }
}