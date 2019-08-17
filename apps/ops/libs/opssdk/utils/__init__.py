#!/usr/bin/env python
# -*-coding:utf-8-*-

import time
from ..logs import Log
log_ins = Log(log_flag='utils')


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        log_ins.write_log("info", '%s execute duration :%.3f second' % (str(func), duration))
        return result
    return wrapper