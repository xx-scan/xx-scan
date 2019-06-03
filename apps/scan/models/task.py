import uuid
from django.db import models

from .scan_cfg import Scheme

ScanTypeChoices = (
    ("service", "服务"),
    ("domain", "域名"),

)


# 进行定时执行的扫描任务:比如今天晚上睡觉了，让它凌晨2点扫出一些数据来。
class ScanTask(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    type = models.CharField(verbose_name="发现类型", default="service", choices=ScanTypeChoices,  max_length=20)
    domains = models.TextField(verbose_name=u"域名名称集合", help_text=u"baidu.com,sina.com.cn", default="baidu.com")

    targets = models.TextField(verbose_name=u"扫描的目标集群", help_text=u"必须是IPv4格式", default="127.0.0.1")
    ports = models.TextField(verbose_name="端口范围", default="1-65535")

    scan_scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, verbose_name="扫描方案", related_name="task_2_scheme")

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    # 制定方案影响的HostService等。

    ## 4中执行类型, 可以都设置，也可以选择设置，u=也可以不设置
    atnow = models.BooleanField(verbose_name=u"立即执行", blank=True)
    regular = models.DateTimeField(verbose_name="定时执行", blank=True)
    interval = models.IntegerField(verbose_name=u"定时扫描", help_text="3600* 2", blank=True)
    crontab = models.CharField(verbose_name=u"Crontab模式", max_length=55, help_text="*/2 * * * *", blank=True)


    def task_run(self):
        """
        任务执行脚本;
        :return:
        """
        pass

    def save(self, *args, **kwargs):
        try:

            super(ScanTask, self).save(*args, **kwargs)
        finally:
            pass

    class Meta:
        db_table = "scan_tasks"
        verbose_name = u"主机服务探测"
