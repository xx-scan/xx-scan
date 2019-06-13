# coding: utf-8
from __future__ import absolute_import, unicode_literals
from celery import shared_task


from ops.celery.decorator import after_app_ready_start, after_app_shutdown_clean_periodic, \
    register_as_period_task

from ops.celery.Task import CustomTask

## http://docs.celeryproject.org/en/latest/userguide/configuration.html#configuration

@shared_task
def print1():
    import time
    time.sleep(10)
    print("=================")
    return "1111111111111111111111111"


@shared_task
def print2(c):
    return "KKK" + c

    # return "OK2222"

@shared_task
def test_chord():
    from celery import shared_task, chain, chord
    chord(header=[print1.s(), ], body=print2.s())()
    # chain()()

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


from ops.celery.decorator import register_as_period_task

@shared_task
@after_app_shutdown_clean_periodic
@register_as_period_task(interval=3600*2)
def pt1():
    print(">>>>>>>>>>>pt1>>>>>>>>>>>")


@shared_task
@after_app_shutdown_clean_periodic
@register_as_period_task(crontab="*/2 * * * *")
def pt2():
    print(">>>>>>>>>>>pt2>>>>>>>>>>>")


