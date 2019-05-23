#!/usr/bin/env python3
# coding: utf-8

import os
import subprocess
import threading
import time
import argparse
import sys
import signal

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

DOCKERD = False

PYTHON_BIN = os.path.join(BASE_DIR, "../cso_venv/bin/python") if not DOCKERD else "/usr/local/bin/python"
CELERY_BIN = os.path.join(BASE_DIR, "../cso_venv/bin/celery") if not DOCKERD else "/usr/local/bin/celery"

GUNICORN_BIN = os.path.join(BASE_DIR, "../cso_venv/bin/gunicorn") if not DOCKERD else "/usr/local/bin/gunicorn"
GUNICORN_CONF_PATH=os.path.join(BASE_DIR, "apps", "gunicorn.conf")

FLOWER_BIN = os.path.join(BASE_DIR, "../cso_venv/bin/flower") if not DOCKERD else "/usr/local/bin/flower"


try:
    from apps.website import const
    __version__ = const.VERSION
except ImportError as e:
    print("Not found __version__: {}".format(e))
    print("Sys path: {}".format(sys.path))
    print("Python is: ")
    print(subprocess.call('which python', shell=True))
    __version__ = 'Unknown'
    try:
        import apps
        print("List apps: {}".format(os.listdir('apps')))
        print('apps is: {}'.format(apps))
    except:
        pass

try:
    from website.conf import load_user_config
    CONFIG = load_user_config()
except ImportError as e:
    print("Import error: {}".format(e))
    print("Could not find config file, `cp config_example.yml config.yml`")
    sys.exit(1)

os.environ["PYTHONIOENCODING"] = "UTF-8"
APPS_DIR = os.path.join(BASE_DIR, 'apps')
LOG_DIR = os.path.join(BASE_DIR, 'logs')
TMP_DIR = os.path.join(BASE_DIR, 'tmp')
HTTP_HOST = CONFIG.HTTP_BIND_HOST or '127.0.0.1'
HTTP_PORT = CONFIG.HTTP_LISTEN_PORT or 8011
DEBUG = CONFIG.DEBUG or False
LOG_LEVEL = CONFIG.LOG_LEVEL or 'INFO'

CELERY_BROKER_URL = 'redis://:%(password)s@%(host)s:%(port)s/%(db)s' % {
    'password': CONFIG.REDIS_PASSWORD,
    'host': CONFIG.REDIS_HOST,
    'port': CONFIG.REDIS_PORT,
    'db': CONFIG.REDIS_DB_CELERY,
}

for _dir in [LOG_DIR, TMP_DIR]:
    if not os.path.exists(_dir):
        os.makedirs(_dir)

START_TIMEOUT = 40
WORKERS = 2
DAEMON = True

EXIT_EVENT = threading.Event()
all_services = ['gunicorn', 'celery', 'beat', 'flower']

try:
    os.makedirs(os.path.join(BASE_DIR, "data", "static"))
    os.makedirs(os.path.join(BASE_DIR, "data", "media"))
except:
    pass


def check_database_connection():
    os.chdir(os.path.join(BASE_DIR, 'apps'))
    for i in range(60):
        print("Check database connection ...")
        code = subprocess.call("{python_bin} manage.py showmigrations auth ".format(python_bin=PYTHON_BIN), shell=True)
        if code == 0:
            print("Database connect success")
            return
        time.sleep(1)
    print("Connection database failed, exist")
    sys.exit(10)


def make_migrations():
    print("Check database structure change ...")
    os.chdir(os.path.join(BASE_DIR, 'apps'))
    print("Migrate model change to database ...")
    subprocess.call('{python_bin} manage.py migrate'.format(python_bin=PYTHON_BIN), shell=True)


def collect_static():
    print("Collect static files")
    os.chdir(os.path.join(BASE_DIR, 'apps'))
    subprocess.call('{python_bin} manage.py collectstatic --no-input'.format(python_bin=PYTHON_BIN), shell=True)


def prepare():
    if not DEBUG:
        check_database_connection()
        make_migrations()
        collect_static()


def get_pid_file_path(service):
    return os.path.join(TMP_DIR, '{}.pid'.format(service))

def get_log_file_path(service):
    return os.path.join(LOG_DIR, '{}.log'.format(service))


def parse_service(s):
    if s == 'all':
        return all_services
    elif "," in s:
        return [i.strip() for i in s.split(',')]
    else:
        return [s]


ServiceDict = {
    "gunicorn" : {
        "welcome":"\n- Start Gunicorn WSGI HTTP Server",
        "start_cmd":[
            GUNICORN_BIN, 'website.wsgi',
            '-b', '{}:{}'.format(HTTP_HOST, HTTP_PORT),
            '-w', str(WORKERS),
            '-p', get_pid_file_path("gunicorn"),
            '--access-logformat', '%(h)s %(t)s "%(r)s" %(s)s %(b)s ',
            '--error-logfile', get_log_file_path("gunicorn"),
            '--log-level', LOG_LEVEL,
            '--access-logfile', '/var/log/hop_srv_access.log'
        ],
        "stop_cmd":"ps -axu | grep 'website.wsgi' | grep -v grep | awk '{print $2}' | xargs kill -15",
        "status_cmd":"ps -axu | grep 'website.wsgi' | grep -v  grep | wc -l"
    },

    "celery": {
        "welcome":"\n- Start Celery as Distributed Task Queue",
        "start_cmd":[
            CELERY_BIN, 'worker',
            '-A', 'ops',
            '-l', 'INFO',
            '--pidfile', get_pid_file_path("celery"),
            '--autoscale', '20,4',
            '--logfile', os.path.join(LOG_DIR, 'celery.log'),
            '--detach',
        ],
        "stop_cmd":"ps -axu | grep 'celery worker' | grep -v grep | awk '{print $2}' | xargs kill -15",
        "status_cmd":"ps -axu | grep 'celery worker' | grep -v  grep | wc -l"
    },

    "beat":{
        "welcome":"\n- Start Beat as Periodic Task Scheduler",
        "start_cmd":[
            CELERY_BIN,  'beat',
            '-A', 'ops',
            '--pidfile', get_pid_file_path('beat'),
            '-l', LOG_LEVEL,
            '--scheduler', "django_celery_beat.schedulers:DatabaseScheduler",
            '--max-interval', '60',
            '--logfile', get_log_file_path('beat'),
            '--detach',
        ],
        "stop_cmd":"ps -axu | grep 'celery beat' | grep -v grep | awk '{print $2}' | xargs kill -15",
        "status_cmd":"ps -axu | grep 'celery beat' | grep -v  grep | wc -l"
    },
    "flower":{
        "welcome":"\n- Start Flower as Periodic Task Scheduler",
        "start_cmd":[
            FLOWER_BIN,
            '--address={}'.format(HTTP_HOST),
            '--port={}'.format(str(CONFIG.FLOWER_BIND_PORT)),
            '--broker={}'.format(CELERY_BROKER_URL),
            '--pidfile={}'.format(get_pid_file_path("flower")),
            '--log-to-stderr={}'.format(get_log_file_path("flower")),
        ],
        "stop_cmd":"ps -axu | grep 'flower' | grep -v grep | awk '{print $2}' | xargs kill -15",
        "status_cmd":"ps -axu | grep 'flower' | grep -v  grep | wc -l"
    },

}


class Service():
    def __init__(self, name="all"):
        self.name = name
        self.start_cmd = ServiceDict[name]["start_cmd"]
        self.stop_cmd = ServiceDict[name]["stop_cmd"]
        self.status_cmd = ServiceDict[name]["status_cmd"]
        self.welcome = ServiceDict[name]["welcome"]
        self.DELAY_LIST = ["flower", ] # flower要延迟生效

    def start(self):
        print(self.welcome)
        # Todo: Must set this environment, otherwise not no ansible result return
        os.environ.setdefault('PYTHONOPTIMIZE', '1')
        if os.getuid() == 0:
            os.environ.setdefault('C_FORCE_ROOT', '1')
        if not self.status():
            if self.name in self.DELAY_LIST:
                time.sleep(9)
            p = subprocess.Popen(self.start_cmd, stdout=sys.stdout, stderr=sys.stderr, cwd=APPS_DIR)
            print("{} 已经启动。".format(self.name))
            return p
        print("{} 正在启动...".format(self.name))


    def stop(self):
        print("{} 关闭".format(self.name))
        time.sleep(2)
        if self.status():
            p = subprocess.Popen(self.stop_cmd, shell=True)
            print("{} 已经停止。".format(self.name))
            return p
        print("{} 正在停止...".format(self.name))


    def status(self, DEBUG=False):
        p = subprocess.Popen(self.status_cmd, cwd=APPS_DIR, shell=True, stdout=subprocess.PIPE)
        _line = p.stdout.read().decode("utf-8").split("\n")[0]
        ## 注意是在shell中进行所有本身占了一行
        # print(_line +"==============" + self.name)
        if int(_line) > 0:
            if DEBUG:
                print("{} 运行中...".format(self.name))
            return True
        else:
            if DEBUG:
                print("{} 已经停止。".format(self.name))
            return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""
        CSO service control tools;

        Example: \r\n

        %(prog)s start all -d;
        """
    )
    parser.add_argument(
        'action', type=str,
        choices=("start", "stop", "restart", "status"),
        help="Action to run"
    )
    parser.add_argument(
        "service", type=str, default="all", nargs="?",
        choices=("all", "gunicorn", "celery", "celery,beat", "flower",),
        help="The service to start",
    )
    parser.add_argument('-d', '--daemon', nargs="?", const=1)
    parser.add_argument('-w', '--worker', type=int, nargs="?", const=2)
    args = parser.parse_args()
    if args.daemon:
        DAEMON = True

    if args.worker:
        WORKERS = args.worker

    action = args.action
    srv = args.service
    services = parse_service(srv)
    if action == "start":
        for service_name in services:
            Service(name=service_name).start()

    elif action == "stop":
        for service_name in services:
            Service(name=service_name).stop()

    elif action == "restart":
        DAEMON = True
        for service_name in services:
            Service(name=service_name).stop()
            time.sleep(10)
            Service(name=service_name).start()
    else:
        for service_name in services:
            Service(name=service_name).status(DEBUG=True)
