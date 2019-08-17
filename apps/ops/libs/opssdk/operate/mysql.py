#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
author : actanble
date   : 2018年2月5日13:37:54
role   : mysql操作
'''
import pymysql
from DBUtils import PooledDB

try:
    from ..logs import Log
    logging = Log(log_flag='pymysql_pool')
except Exception as e:
    import logging
    logging.error(e)

from ..configs import config_templates


class MysqlPool:

    def __init__(self, config_template=config_templates, *args, **kwargs):
        self.config = {
            'creator': pymysql,
            'host': config_template['MYSQL']['HOST'],
            'port': config_template['MYSQL']['PORT'],
            'user': config_template['MYSQL']['USER'],
            'password': config_template['MYSQL']['PASSWD'],
            'db': config_template['MYSQL']['DB'],
            'charset': config_template['MYSQL']['CHARSET'],
            'maxconnections': 70,
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.pool = PooledDB(**self.config)

    def __enter__(self):
        try:
            self.conn = self.pool.connection()
            self.cursor = self.conn.cursor()
        except:
            raise ValueError('mysql connect error {0}'.format(self.host))
        return self

    # 释放资源
    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

    #  查询
    def query(self, sql):
        try:
            with self:
                self.cursor.execute(sql)
                res = self.cursor.fetchall()
        except Exception as e:
            logging.error("error", e)
            raise e

        return res

    def change(self, sql):
        resnum = 0
        try:
            with self:
                resnum = self.cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            # 错误回滚
            logging.error("error", e)
            self.conn.rollback()
        return resnum