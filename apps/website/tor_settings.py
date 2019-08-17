#!/usr/bin/env python
# -*-coding:utf-8-*-

import os
from ops.libs.websdk.consts import const

ROOT_DIR = os.path.dirname(__file__)
debug = True
xsrf_cookies = False
expire_seconds = 365 * 24 * 60 * 60
cookie_secret = '61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2X6TP1o/Vo='

sign_name = 'CSO客户端监控任务加密认证工具',
template_code = 'CSO_AGENTX_190811',

DEFAULT_REDIS_HOST = os.getenv('DEFAULT_REDIS_HOST', '172.16.0.223')
DEFAULT_REDIS_PORT = os.getenv('DEFAULT_REDIS_PORT', '6379')
DEFAULT_REDIS_DB = 6
DEFAULT_REDIS_AUTH = True
DEFAULT_REDIS_CHARSET = 'utf-8'
DEFAULT_REDIS_PASSWORD = os.getenv('DEFAULT_REDIS_PASSWORD', '123456')

DEFAULT_MQ_ADDR = os.getenv('DEFAULT_MQ_ADDR', '172.16.0.223')
DEFAULT_MQ_PORT = 5672
DEFAULT_MQ_VHOST = '/'
DEFAULT_MQ_USER = os.getenv('DEFAULT_MQ_USER', 'yz')
DEFAULT_MQ_PWD = os.getenv('DEFAULT_MQ_PWD', 'vuz84B2IkbEtXWF')

# try:
#     from local_settings import *
# except:
#     pass

from .settings import CONFIG
"""
CELERY_BROKER_URL = 'redis://:%(password)s@%(host)s:%(port)s/%(db)s' % {
    'password': CONFIG.REDIS_PASSWORD,
    'host': CONFIG.REDIS_HOST,
    'port': CONFIG.REDIS_PORT,
    'db': CONFIG.REDIS_DB_CELERY,
}
"""
settings = dict(
    debug=debug,
    xsrf_cookies=xsrf_cookies,
    cookie_secret=cookie_secret,
    expire_seconds=expire_seconds,
    sign_name=sign_name,
    template_code=template_code,
    app_name='cso_agentx',
    databases={
        const.DEFAULT_DB_KEY: {
            const.DBHOST_KEY: CONFIG.DB_HOST,
            const.DBPORT_KEY: CONFIG.DB_PORT,
            const.DBUSER_KEY: CONFIG.DB_USER,
            const.DBPWD_KEY: CONFIG.DB_PASSWORD,
            const.DBNAME_KEY: CONFIG.DB_NAME,
        },
    },
    redises={
        const.DEFAULT_RD_KEY: {
            const.RD_HOST_KEY: CONFIG.REDIS_HOST,
            const.RD_PORT_KEY: CONFIG.REDIS_PORT,
            const.RD_DB_KEY: CONFIG.REDIS_DB_TORNADO,
            const.RD_AUTH_KEY: DEFAULT_REDIS_AUTH,
            const.RD_CHARSET_KEY: DEFAULT_REDIS_CHARSET,
            const.RD_PASSWORD_KEY: CONFIG.REDIS_PASSWORD
        }
    },
    mqs={
        const.DEFAULT_MQ_KEY: {
            const.MQ_ADDR: CONFIG.MQ_ADDR,
            const.MQ_PORT: CONFIG.MQ_PORT,
            const.MQ_VHOST: CONFIG.MQ_VHOST,
            const.MQ_USER: CONFIG.MQ_USER,
            const.MQ_PWD: CONFIG.MQ_PWD,
        }
    }
)

import sys
import django
# Add Django ORM
DjangoModulePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DjangoModulePath)
os.chdir(DjangoModulePath)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
django.setup()
