from django.db import models


class CronLog(models.Model):

    log_id = models.AutoField('log_id', primary_key=True)
    job_id = models.CharField('job_id', max_length=255)
    status = models.CharField('task_cmd', max_length=10)
    task_cmd = models.CharField('task_cmd', max_length=150)
    task_log = models.TextField('task_log')
    exec_time = models.DateTimeField(auto_now_add=True, verbose_name='执行时间')

    class Meta:
        db_table = "cron_log"
        verbose_name = "Cron执行日志"
        ordering = ('-exec_time',)


# 任务日志表
class TaskLog(models.Model):
    log_id = models.AutoField('log_id', primary_key=True)
    log_key = models.CharField('log_key', max_length=150)
    task_level = models.IntegerField()
    log_info = models.TextField()
    exec_time = models.BigIntegerField()
    log_time = models.DateTimeField(auto_now_add=True, verbose_name='执行时间')

    class Meta:
        db_table = "scheduler_task_log"
        verbose_name = "scheduler_task 执行日志"
        ordering = ('-log_time', '-task_level')