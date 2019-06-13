from __future__ import absolute_import, unicode_literals
from django_celery_beat.models import (
  PeriodicTask, IntervalSchedule, CrontabSchedule
)



from xadmin.sites import site
site.register(IntervalSchedule) # 存储循环任务设置的时间
site.register(CrontabSchedule) # 存储定时任务设置的时间
site.register(PeriodicTask) # 存储任务
# site.register(TaskState) # 存储任务执行状态
# site.register(WorkerState) # 存储执行任务的worker