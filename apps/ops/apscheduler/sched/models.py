# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class CronConfig(models.Model):
    cron_second = models.CharField(max_length=10, verbose_name='分', default='*')
    cron_minute = models.CharField(max_length=10, verbose_name='分', default='*')
    cron_hour = models.CharField(max_length=10, verbose_name='时', default='*')
    cron_day = models.CharField(max_length=10, verbose_name='天', default='*')
    cron_month = models.CharField(max_length=10, verbose_name='月', default='*')
    cron_week = models.CharField(max_length=10, verbose_name='周', default='*')
    cron_name = models.CharField(max_length=100, verbose_name='Cron名称', default='every 1 second', unique=True)
    # cron_status = models.SmallIntegerField(verbose_name='任务状态', default=None)

    class Meta:
        db_table = 'opsmanage_cron_config'
        verbose_name = 'Cron配置'
