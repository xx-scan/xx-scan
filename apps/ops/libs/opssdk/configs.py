import os

LINUX_LOG_DIR = "/opt/log/"
WIN_LOG_DIR = "e://log/"

if not os.path.exists(LINUX_LOG_DIR):
    os.makedirs(LINUX_LOG_DIR)

if not os.path.exists(WIN_LOG_DIR):
    os.makedirs(WIN_LOG_DIR)


class CONFIG:
    DB_NAME = 'devops'
    DB_HOST = "localhost"
    DB_PORT = 3306
    DB_USER = "root"
    DB_PASSWORD = "test@1q2w2e4R"


try:
    from website.settings import CONFIG
except:
    from .logs import Log
    logger = Log(log_flag='run')
    logger.error('没有`websiste`目录，可能是没启动`Django`或者没有`website.settings`')


config_templates = dict(
    MYSQL={
        'NAME': CONFIG.DB_NAME,
        'HOST': CONFIG.DB_HOST,
        'PORT': CONFIG.DB_PORT,
        'USER': CONFIG.DB_USER,
        'PASSWD': CONFIG.DB_PASSWORD,
        'CHARSET': CONFIG.DB_CHARSET,
    }
)