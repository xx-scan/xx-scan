import uuid
from django.db import models

from .scan_cfg import Scheme


# 进行定时执行的扫描任务:比如今天晚上睡觉了，让它凌晨2点扫出一些数据来。
class ScanTask(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    targets = models.TextField(verbose_name="扫描的目标集群", help_text="必须是IPv4格式")
    scan_scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE,
                        verbose_name="", related_name="task_2_scheme")

    scan_interval = models.IntegerField(verbose_name="Crontab扫描",
                                        help_text="*/2 * * * *", default=3600*24)
    scan_crontab = models.CharField(verbose_name="Crontab扫描", max_length=55,
                                    help_text="*/2 * * * *", default="0 0 * * *")

    class Meta:
        db_table = "scan_tasks"
        verbose_name = "主机服务探测"
