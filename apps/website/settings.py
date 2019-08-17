import os
import sys


from .conf import load_user_config
from . import const
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_DIR)

CONFIG = load_user_config()
DOCKERD = True

LOG_DIR = os.path.join(PROJECT_DIR, 'logs')
CSO_LOG_FILE = os.path.join(LOG_DIR, 'cso.log')
ANSIBLE_LOG_FILE = os.path.join(LOG_DIR, 'ansible.log')
GUNICORN_LOG_FILE = os.path.join(LOG_DIR, 'gunicorn.log')

VERSION = const.VERSION

if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used fips production secret!
SECRET_KEY = CONFIG.SECRET_KEY

# SECURITY WARNING: keep the token secret, remove it if all coco, guacamole ok
BOOTSTRAP_TOKEN = CONFIG.BOOTSTRAP_TOKEN

# SECURITY WARNING: don't run with debug turned on fips production!
DEBUG = CONFIG.DEBUG
STATIC_USE_CDN = CONFIG.STATIC_USE_CDN

# Absolute url for some case, for example email link
if DEBUG:
    SITE_URL = 'http://localhost:3322'
else:
    SITE_URL = CONFIG.SITE_URL


# LOG LEVEL
LOG_LEVEL = CONFIG.LOG_LEVEL

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'corsheaders',

    # 'django_celery_beat',
]

INSTALLED_APPS += ["secs.apps.LocalAppConfig", "ops.apps.LocalAppConfig"]
INSTALLED_APPS += ["scan.apps.LocalAppConfig", ]

# Add apscheduler
INSTALLED_APPS += ['django_apscheduler.apps.DjangoApschedulerConfig']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
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
                # 'accounts.context_processors.seo_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'website.wsgi.application'
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
    },
    # 'mongo': {
    #     'ENGINE': None,
    # }
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

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_TIME_FORMAT = '%Y-%m-%d'


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

if sys.platform == 'win32':
    STATIC_ROOT = 'E:\\xadmin\\collect_static\\'


STATIC_URL = '/static/'
STATICFILES = os.path.join(BASE_DIR, 'static')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# Email-settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_HOST = 'smtp.163.com'
EMAIL_HOST_USER = 'actanble@163.com'
EMAIL_HOST_PASSWORD = 'string123'
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

MEDIA_DIR = os.path.join(STATIC_ROOT, 'media')

if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

MEDIA_URL = '/static/uploads/'
MEDIA_ROOT = os.path.join(MEDIA_DIR, 'collect_static', 'uploads')

# PROJECT_DIR = STATIC_ROOT
# import pymysql

SITE_TITLE = u'信息安全管控平台'

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

CELERYD_FORCE_EXECV = True     # 非常重要,有些情况下可以防止死锁
CELERY_WORKER_CONCURRENCY = 1
CELERYD_CONCURRENCY = 20  # 并发worker数

# 2019-6-25 设置 interval 出错加上 celery_timezone
CELERY_TIMEZONE = TIME_ZONE
CELERYD_PREFETCH_MULTIPLIER = 1
CELERYD_MAX_TASKS_PER_CHILD = 100 

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_TASK_ALWAYS_EAGER = False
CELERY_WORKER_HIJACK_ROOT_LOGGER = False
CELERY_TASK_ACKS_LATE = True  # Retry if task fails
CELERY_TASK_TIME_LIMIT = 60 * 25  # fips seconds, so 25 minutes
CELERY_SEND_TASK_ERROR_EMAILS = False

CELERY_ALWAYS_EAGER = False
CELERY_ACKS_LATE = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_DISABLE_RATE_LIMITS = False


# Cache use redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # 'BACKEND': 'redis_cache.cache.RedisCache',
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

# Load Cor Headers 
X_FRAME_OPTIONS = 'ALLOWALL'

# 跨域增加忽略
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ('*')
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'Authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
    'X-Token',
)

SESSION_COOKIE_AGE = 60 * 30  # 30分钟
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 关闭浏览器，则COOKIE失效

# 取消CSRF中间件
MIDDLEWARE.append('secs.middle.MiddleWare.DisableCSRFCheck')
if DEBUG:
    MIDDLEWARE.append('secs.middle.MiddleWare.SiteMainMiddleware')

PREVILEGED_USER_SETS = ["admin001", "admin007"]
