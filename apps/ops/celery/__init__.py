# -*- coding: utf-8 -*-

import os

from celery import Celery

# Todo: Set ENV and autodiscover_tasks based in django-beat
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

# from website import settings
from website import settings

# from django.conf import settings

app = Celery('xxscan')


configs = {k: v for k, v in settings.__dict__.items() if k.startswith('CELERY')}
app.namespace = 'CELERY'
app.conf.update(configs)

# print([app_config.split('.')[0] for app_config in INSTALLED_APPS])
app.autodiscover_tasks(lambda: [app_config.split('.')[0] for app_config in settings.INSTALLED_APPS] )