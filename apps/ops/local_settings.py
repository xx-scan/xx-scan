#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import os
import types
import errno
import json
import yaml
from importlib import import_module

CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "")


def import_string(dotted_path):
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
                          ) from err


class Config(dict):

    def __init__(self, root_path=None, defaults=None):
        self.defaults = defaults or {}
        self.root_path = root_path
        super().__init__({})

    def from_envvar(self, variable_name, silent=False):
        rv = os.environ.get(variable_name)
        if not rv:
            if silent:
                return False
            raise RuntimeError('The environment variable %r is not set '
                               'and as such configuration could not be '
                               'loaded.  Set this variable and make it '
                               'point to a configuration file' %
                               variable_name)
        return self.from_pyfile(rv, silent=silent)

    def from_pyfile(self, filename, silent=False):
        if self.root_path:
            filename = os.path.join(self.root_path, filename)
        d = types.ModuleType('config')
        d.__file__ = filename
        try:
            with open(filename, mode='rb') as config_file:
                exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        self.from_object(d)
        return True

    def from_object(self, obj):
        if isinstance(obj, str):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)

    def from_json(self, filename, silent=False):
        if self.root_path:
            filename = os.path.join(self.root_path, filename)
        try:
            with open(filename) as json_file:
                obj = json.loads(json_file.read())
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        return self.from_mapping(obj)

    def from_yaml(self, filename, silent=False):
        if self.root_path:
            filename = os.path.join(self.root_path, filename)
        try:
            with open(filename, 'rt', encoding='utf8') as f:
                obj = yaml.load(f)
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        if obj:
            return self.from_mapping(obj)
        return True

    def from_mapping(self, *mapping, **kwargs):
        mappings = []
        if len(mapping) == 1:
            if hasattr(mapping[0], 'items'):
                mappings.append(mapping[0].items())
            else:
                mappings.append(mapping[0])
        elif len(mapping) > 1:
            raise TypeError(
                'expected at most 1 positional argument, got %d' % len(mapping)
            )
        mappings.append(kwargs.items())
        for mapping in mappings:
            for (key, value) in mapping:
                if key.isupper():
                    self[key] = value
        return True

    def get_namespace(self, namespace, lowercase=True, trim_namespace=True):
        rv = {}
        for k, v in self.items():
            if not k.startswith(namespace):
                continue
            if trim_namespace:
                key = k[len(namespace):]
            else:
                key = k
            if lowercase:
                key = key.lower()
            rv[key] = v
        return rv

    def convert_type(self, k, v):
        default_value = self.defaults.get(k)
        if default_value is None:
            return v
        tp = type(default_value)
        try:
            v = tp(v)
        except Exception:
            pass
        return v

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, dict.__repr__(self))

    def __getitem__(self, item):
        # 先从设置的来
        try:
            value = super().__getitem__(item)
        except KeyError:
            value = None
        if value is not None:
            return self.convert_type(item, value)
        # 其次从环境变量来
        value = os.environ.get(item, None)
        if value is not None:
            if value.lower() == 'false':
                value = False
            elif value.lower() == 'true':
                value = True
            return self.convert_type(item, value)
        return self.defaults.get(item)

    def __getattr__(self, item):
        return self.__getitem__(item)


defaults = dict(
    MYSQL_PASSWORD="m9uSFL7duAVXfeAwGUSG",
    MYSQL_ROOT_PASSWORD="m9uSFL7duAVXfeAwGUSG",
    MYSQL_ROOT_USER="root",
    MYSQL_SERVER_PORT=3306,
    MYSQL_SERVER_DB="agentx",
    REDIS_PASSWORD="cWCVKJ7ZHUK12mVbivUf",
    cookie_secret="nJ2oZis0V/xlArY2rzpIE6ioC9/KlqR2fd59sD=UXZJ=3OeROB",
    token_secret="pXFb4i%*834gfdh963df713iodGq4dsafsdadg7yI6ImF1999aaG7",
    DEFAULT_DB_DBHOST="192.169.2.228",
    DEFAULT_DB_DBPORT=3306,
    DEFAULT_DB_DBUSER="root",
    MQ_USER="root",
    MQ_PASSWORD="test@1q2w2e4R",
    DEFAULT_DB_DBPWD="m9uSFL7duAVXfeAwGUSG",
    DEFAULT_DB_DBNAME="codo",
    DEFAULT_REDIS_HOST="192.169.2.228",
    DEFAULT_REDIS_PORT="6379",
    DEFAULT_REDIS_PASSWORD="cWCVKJ7ZHUK12mVbivUf",
    MYSQL_HOST="192.169.2.228",
    REDIS_HOST="192.169.2.228",
    MQ_HOST="192.169.2.228",
    REDIS_PORT=6379,
    MONGO_HOST="192.169.2.228",
    MONGO_PORT=27017,
    MONGO_USER="admin007",
    MONGO_PASS="myadmin@816",
    MONGO_AUTH_DB="admin",
)


def load_from_object(config):
    try:
        from config import config as c
        config.from_object(c)
        return True
    except ImportError:
        pass
    return False


def load_from_yml(config):
    for i in ['config.yml', 'config.yaml']:
        if not os.path.isfile(os.path.join(config.root_path, i)):
            continue
        loaded = config.from_yaml(i)
        if loaded:
            return True
    return False


def load_user_config():
    # sys.path.insert(0, APPS_DIR)
    config = Config(CONFIG_DIR, defaults)

    loaded = load_from_object(config)
    if not loaded:
        loaded = load_from_yml(config)
    if not loaded:
        msg = """
        Error: No config file found.
        You can run `cp config_example.yml config.yml`, and edit it.
        """
        raise ImportError(msg)
    return config


CONFIG = load_user_config()


MYSQL_PASSWORD = CONFIG.MYSQL_PASSWORD
MYSQL_ROOT_USER = CONFIG.MYSQL_ROOT_USER
MYSQL_SERVER_PORT = CONFIG.MYSQL_SERVER_PORT
MYSQL_SERVER_DB = CONFIG.MYSQL_SERVER_DB
REDIS_PASSWORD = CONFIG.REDIS_PASSWORD
REDIS_PORT = CONFIG.REDIS_PORT
cookie_secret = CONFIG.cookie_secret
token_secret = CONFIG.token_secret

# MYSQL设置 数据库密码随着生成
MYSQL_ROOT_PASSWORD = MYSQL_PASSWORD
DEFAULT_DB_DBHOST = CONFIG.MYSQL_HOST
DEFAULT_DB_DBPORT = MYSQL_SERVER_PORT
DEFAULT_DB_DBUSER = MYSQL_ROOT_USER
DEFAULT_DB_DBPWD = MYSQL_PASSWORD
DEFAULT_DB_DBNAME = MYSQL_SERVER_DB

# Redis 设置
DEFAULT_REDIS_HOST = CONFIG.REDIS_HOST
DEFAULT_REDIS_PORT = REDIS_PORT
DEFAULT_REDIS_PASSWORD = REDIS_PASSWORD
DEFAULT_REDIS_DB = 8
DEFAULT_REDIS_AUTH = True
DEFAULT_REDIS_CHARSET = 'utf-8'

DEFAULT_MQ_ADDR = CONFIG.MQ_HOST
MQ_USER = CONFIG.MQ_USRE
MQ_PASSWORD = CONFIG.MQ_PASSWORD
RABBITMQ_DEFAULT_USER = MQ_USER
RABBITMQ_DEFAULT_PASS = MQ_PASSWORD
DEFAULT_MQ_PORT = 5672
DEFAULT_MQ_VHOST = '/'

DEFAULT_MONGO_HOST = CONFIG.MONGO_HOST
DEFAULT_MONGO_PORT = CONFIG.MONGO_PORT
DEFAULT_MONGO_USER = CONFIG.MONGO_USER
DEFAULT_MONGO_PASS = CONFIG.MONGO_PASS
DEFAULT_MONGO_AUTH_DB = CONFIG.MONGO_AUTH_DB