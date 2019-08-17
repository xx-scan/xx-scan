#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
author : actanble
date   : 2018年2月5日13:37:54
role   : mysql操作
'''

import pymysql
from opssdk.logs import Log
from django.db import connection, transaction


class DjangoSqlConn:

    @staticmethod
    def fetch(sql):
        with connection.cursor() as cursor:
            cursor.execute(sql)
            yield cursor.fetchall()

    # @transaction.on_commit
    # def commit(self, sql):
    #     from django.db import connection, transaction
    #     cursor = connection.cursor()
    #     yield cursor.execute(sql)
    #     cursor.commit()


# 2019-8-13 强转失败