import os
import sys


from .conf import load_user_config
from . import const
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_DIR)

CONFIG = load_user_config()

LOG_DIR = os.path.join(PROJECT_DIR, 'logs')
XXSCAN_LOG_FILE = os.path.join(LOG_DIR, 'xxscan.log')
ANSIBLE_LOG_FILE = os.path.join(LOG_DIR, 'ansible.log')
GUNICORN_LOG_FILE = os.path.join(LOG_DIR, 'gunicorn.log')\

VERSION = const.VERSION

if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG.SECRET_KEY

# SECURITY WARNING: keep the token secret, remove it if all coco, guacamole ok
BOOTSTRAP_TOKEN = CONFIG.BOOTSTRAP_TOKEN

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.DEBUG

# Absolute url for some case, for example email link
SITE_URL = CONFIG.SITE_URL

# LOG LEVEL
LOG_LEVEL = CONFIG.LOG_LEVEL

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [

    'jet.dashboard',
    'jet',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'corsheaders',

    'django_celery_beat',
]

INSTALLED_APPS += ["services.apps.LocalAppConfig", "scan.apps.LocalAppConfig"]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 全局过滤器全部舍弃
                #'accounts.context_processors.seo_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'website.wsgi.application'

# Logging setting
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'main': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '%(asctime)s [%(module)s %(levelname)s] %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'msg': {
            'format': '%(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'main'
        },
        'file': {
            'encoding': 'utf8',
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*100,
            'backupCount': 7,
            'formatter': 'main',
            'filename': XXSCAN_LOG_FILE,
        },
        'ansible_logs': {
            'encoding': 'utf8',
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'main',
            'maxBytes': 1024*1024*100,
            'backupCount': 7,
            'filename': ANSIBLE_LOG_FILE,
        },
        'gunicorn_file': {
            'encoding': 'utf8',
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'msg',
            'maxBytes': 1024*1024*100,
            'backupCount': 2,
            'filename': GUNICORN_LOG_FILE,
        },
        'gunicorn_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'msg'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': False,
            'level': LOG_LEVEL,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        # 'django.db': {
        #     'handlers': ['console', 'file'],
        #     'level': 'DEBUG'
        # }
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

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# Session 和y页面的缓存存储, 由于不是ORM，所以很多用户上

SESSION_COOKIE_DOMAIN = CONFIG.SESSION_COOKIE_DOMAIN
CSRF_COOKIE_DOMAIN = CONFIG.CSRF_COOKIE_DOMAIN
SESSION_COOKIE_AGE = CONFIG.SESSION_COOKIE_AGE
SESSION_EXPIRE_AT_BROWSER_CLOSE = CONFIG.SESSION_EXPIRE_AT_BROWSER_CLOSE
SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS = {
    'host': CONFIG.REDIS_HOST,
    'port': CONFIG.REDIS_PORT,
    'password': CONFIG.REDIS_PASSWORD,
    'db': CONFIG.REDIS_DB_SESSION,
    'prefix': 'auth_session',
    'socket_timeout': 1,
    'retry_on_timeout': False
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DB_OPTIONS = {}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.{}'.format(CONFIG.DB_ENGINE.lower()),
        'NAME': CONFIG.DB_NAME,
        'HOST': CONFIG.DB_HOST,
        'PORT': CONFIG.DB_PORT,
        'USER': CONFIG.DB_USER,
        'PASSWORD': CONFIG.DB_PASSWORD,
        'ATOMIC_REQUESTS': True,
        'OPTIONS': DB_OPTIONS
    }
}

DB_CA_PATH = os.path.join(PROJECT_DIR, 'data', 'ca.pem')
if CONFIG.DB_ENGINE.lower() == 'mysql':
    # DB_OPTIONS['init_command'] = "SET sql_mode='STRICT_TRANS_TABLES'"
    DB_OPTIONS['sql_mode'] = "traditional"
    if os.path.isfile(DB_CA_PATH):
        DB_OPTIONS['ssl'] = {'ca': DB_CA_PATH}

# I18N translation
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# restframework
from .restframework import *
INSTALLED_APPS += REST_FRAMEWORK_APPS

# Custom User Auth model
#AUTH_USER_MODEL = 'users.User'

# File Upload Permissions
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755


SITE_ID = 1
SITE_ROOT = os.path.dirname(BASE_DIR)
STATIC_ROOT = os.path.join(SITE_ROOT, 'collect_static')

STATIC_URL = '/static/'
STATICFILES = os.path.join(BASE_DIR, 'static')

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_TIME_FORMAT = '%Y-%m-%d'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


### Email-settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_HOST = 'smtp.163.com'
EMAIL_HOST_USER = 'test@163.com'
EMAIL_HOST_PASSWORD = 'tset222'
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

#from .site_settings.logsettings import LOGGING

# from .site_settings.cors import *
MEDIA_DIR = STATIC_ROOT
if sys.platform == 'win32':
    MEDIA_DIR = "e://"

if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

MEDIA_URL = '/static/uploads/'
MEDIA_ROOT = os.path.join(MEDIA_DIR, 'collect_static', 'uploads')

# PROJECT_DIR = STATIC_ROOT
# import pymysql

SITE_TITLE = u'XX-SCAN'

# Dump all celery log to here
CELERY_LOG_DIR = os.path.join(PROJECT_DIR, 'data', 'celery')

# Celery using redis as broker
CELERY_BROKER_URL = 'redis://:%(password)s@%(host)s:%(port)s/%(db)s' % {
    'password': CONFIG.REDIS_PASSWORD,
    'host': CONFIG.REDIS_HOST,
    'port': CONFIG.REDIS_PORT,
    'db': CONFIG.REDIS_DB_CELERY,
}

CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json', 'pickle']
CELERY_RESULT_EXPIRES = 3600
# CELERY_WORKER_LOG_FORMAT = '%(asctime)s [%(module)s %(levelname)s] %(message)s'
# CELERY_WORKER_LOG_FORMAT = '%(message)s'
# CELERY_WORKER_TASK_LOG_FORMAT = '%(task_id)s %(task_name)s %(message)s'
CELERY_WORKER_TASK_LOG_FORMAT = '%(message)s'
# CELERY_WORKER_LOG_FORMAT = '%(asctime)s [%(module)s %(levelname)s] %(message)s'
CELERY_WORKER_LOG_FORMAT = '%(message)s'
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_WORKER_REDIRECT_STDOUTS = True
CELERY_WORKER_REDIRECT_STDOUTS_LEVEL = "INFO"
# CELERY_WORKER_HIJACK_ROOT_LOGGER = True
CELERY_WORKER_MAX_TASKS_PER_CHILD = 40
CELERY_TASK_SOFT_TIME_LIMIT = 3600

CELERYD_FORCE_EXECV = True
CELERY_WORKER_CONCURRENCY = 1

# Cache use redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        #'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': 'redis://:%(password)s@%(host)s:%(port)s/%(db)s' % {
            'password': CONFIG.REDIS_PASSWORD,
            'host': CONFIG.REDIS_HOST,
            'port': CONFIG.REDIS_PORT,
            'db': CONFIG.REDIS_DB_CACHE,
        },
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

try:
    import pymysql
    MPP_CONFIG = {
        'host': DATABASES["default"]["HOST"],
        'port': DATABASES["default"]["PORT"],
        'user': DATABASES["default"]["USER"],
        'password': DATABASES["default"]["PASSWORD"],
        'db': DATABASES["default"]["NAME"],
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor,
    }
except:
    pass


## 取消CSRF中间件
MIDDLEWARE.append('services.middle.MiddleWare.DisableCSRFCheck')
MIDDLEWARE.append('services.middle.MiddleWare.SiteMainMiddleware')

