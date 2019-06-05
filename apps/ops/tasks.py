# coding: utf-8
from __future__ import absolute_import, unicode_literals
import os
import subprocess

from django.conf import settings
from celery import shared_task, subtask
from celery.exceptions import SoftTimeLimitExceeded
from django.utils import timezone


from .celery.decorator import (
    register_as_period_task, after_app_shutdown_clean_periodic,
    after_app_ready_start
)
from .celery.utils import create_or_update_celery_periodic_tasks


@shared_task
@after_app_ready_start
def create_or_update_registered_periodic_tasks():
    from .celery.decorator import get_register_period_tasks
    for task in get_register_period_tasks():
        create_or_update_celery_periodic_tasks(task)