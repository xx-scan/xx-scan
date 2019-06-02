from celery import Task
from celery.result import AsyncResult

from celery import chain, chord
from datetime import datetime


class CustomTask(Task):

    def on_success(self, retval, task_id, args, kwargs):

        print('task done: {0}'.format(retval))
        from datetime import datetime

        return super(CustomTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('task fail, reason: {0}'.format(exc))
        return super(CustomTask, self).on_failure(exc, task_id, args, kwargs, einfo)