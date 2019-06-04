import sys
from datetime import datetime

import pymongo
try:
    from xsqlmb.settings import MongoConfig
except:
    MongoConfig = dict(host='localhost', port=27017, db_name='wafOpt', username=None, password=None)


class MongoConn(object):
    def __init__(self, MONGODB_CONFIG=MongoConfig):
        self.MONGODB_CONFIG = MONGODB_CONFIG
        # connect db
        try:
            self.conn = pymongo.MongoClient(self.MONGODB_CONFIG['host'], self.MONGODB_CONFIG['port'])
            self.db = self.conn[self.MONGODB_CONFIG['db_name']]  # connect db
            self.username=self.MONGODB_CONFIG['username']
            self.password=self.MONGODB_CONFIG['password']
            if self.username and self.password:
                self.connected = self.db.authenticate(self.username, self.password)
            else:
                self.connected = True
        except Exception as e:
            print(e)
            sys.exit(1)

    def show_data(self, table='nginx_access_log'):
        my_conn = MongoConn()
        res = my_conn.db[table].find(projection={"_id":False})
        for x in res:
            print(x)

    def insert_data(self, table, data):
        from datetime import datetime
        syslog_stat = {"pre_data_len": len(data),
                       "opt_table": table,
                       "stat": "NoneExcept",
                       "runtime": str(datetime.now())}
        try:
            self.db[table].insert(data)
        except:
            pass
        finally:
            self.db["actionlog"].insert(syslog_stat)

    def insert_data_uniq(self, table, data, key="audit_logid"):
        # import numpy as np
        try:
            mongo_saved_data = [data[key] for data in self.db[table].find({})]
        except:
            mongo_saved_data = []
        res_data = [item for item in data if item[key] not in mongo_saved_data]
        ## 无重插入
        from datetime import datetime
        syslog_stat = {"pre_data_len": len(data), "opt_table": table, "stat": "Insert【" + str(len(res_data)) + "】条数据", "runtime": str(datetime.now())}
        try:
            self.db[table].insert(res_data)
        except:
            pass
        finally:
            self.db["actionlog"].insert(syslog_stat)

    def show_actions_logs(self):
        # return self.db["actionlog"].find()
        for x in self.db["actionlog"].find():
            print(x)

    def remove(self, table):
        self.db[table].remove()

    def show_by_condition(self, table, condition={}):
        # 根据条件进行查询，返回所有记录
        res = self.db[table].find(condition)
        for x in res:
            print(x)

    def show_actions(self):
        for x in self.db["actionlog"].find():
            print(x)

    def query_timestamp_datas(self, table_name):
        ScriptAuditLogTable = "script_log"
        _script_log = list(self.db[ScriptAuditLogTable].find(
            {"table_name": table_name}).sort([("last_time", pymongo.DESCENDING, )]) )
        if len(_script_log) > 0 :
            _last_run_time = _script_log[0]["last_time"]
        else:
            _last_run_time = datetime(1993,9,27,11,12,3)

        data = list( self.db[table_name].find({"time":{"$gt": _last_run_time} }) )
        data0 = list( self.db[table_name].find({"time":{"$gt": _last_run_time} }).sort([("time", pymongo.DESCENDING, )]) )

        if len(data) < 1:
            return None
        _timestamp = data0[0]["time"]
        try:
            return data
        finally:
            self.db[ScriptAuditLogTable].insert(dict(
                table_name=table_name,
                last_time=_timestamp
            ))
