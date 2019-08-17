#!/usr/bin/env python
# -*-coding:utf-8-*-


from urllib.parse import quote_plus
from website.tor_settings import settings


def get_db_url(dbkey):
    databases = settings.get('databases', 0)
    db_conf = databases[dbkey]
    dbuser = db_conf['user']
    dbpwd = db_conf['pwd']
    dbhost = db_conf['host']
    dbport = db_conf.get('port', 0)
    dbname = db_conf['name']
    url = 'mysql+pymysql://{user}:{pwd}@{host}:{port}/{dbname}?charset=utf8'.format(
        user=dbuser, pwd=quote_plus(dbpwd), host=dbhost, port=dbport, dbname=dbname)
    return url


def get_mongo_client(dbkey="mongodb"):
    databases = settings.get('mongodb', 0)
    db_conf = databases[dbkey]
    from pymongo import MongoClient
    return MongoClient(
        db_conf["host"],
        username=db_conf["username"],
        password=quote_plus(db_conf["password"]),
        authSource=db_conf["auth_db"],
        authMechanism='SCRAM-SHA-256'
    )