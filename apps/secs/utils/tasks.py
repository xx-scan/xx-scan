# coding: utf-8
from celery import shared_task
from ops.celery.decorator import after_app_ready_start, after_app_shutdown_clean_periodic, \
    register_as_period_task

from ops.celery.Task import CustomTask

## http://docs.celeryproject.org/en/latest/userguide/configuration.html#configuration

@shared_task
def hello():
    from datetime import datetime

    print("=========="+ str(datetime.now()) +"===========")

    print("============")

    import time
    time.sleep(3)

    # return "OK"

@shared_task
#@after_app_shutdown_clean_periodic
@register_as_period_task(interval=1)
def test2():
    print("=============fdsafdsa========")
    # return "OK2222"

@shared_task(base=CustomTask)
#@after_app_shutdown_clean_periodic
#@register_as_period_task(interval=1)
def test():
    print("==fdsafdsa=f=dsa=f=dsa=fd=saf=dsa=fd=sa=fdsa")

    return ["test_2019_customer_task", "中国"]

@shared_task
def print1():
    print("=================")
    return "1111111111111111111111111"


@shared_task
def print2(c):
    return "KKK" + c

    # return "OK2222"

# from celery.schedules import crontab
# from conf.celery import app
# # http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#crontab-schedules
# app.conf.beat_schedule = {
#     # Executes every Monday morning at 7:30 a.m.
#     'add-every-monday-morning': {
#         'task': 'tasks.add',
#         'schedule': crontab(hour=7, minute=30, day_of_week=1),
#         'args': (16, 16),
#     },
# }
#

## https://www.cnblogs.com/wdliu/p/9517535.html
## group chmod chain



