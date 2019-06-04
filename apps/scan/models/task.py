import uuid
from django.db import models

from .scan_cfg import Scheme
from .workspace import Workspace


ScanTypeChoices = (
    ("service", "服务"),
    ("domain", "域名"),

)

from .http import PortRange


class ScanTask(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    type = models.CharField(verbose_name="发现类型", default="service", choices=ScanTypeChoices,  max_length=20)
    domains = models.TextField(verbose_name=u"域名名称集合", help_text=u"baidu.com,sina.com.cn", default="baidu.com")

    imports_active = models.BooleanField(verbose_name="开启文件导入方式", default=False)
    imports = models.FileField(upload_to="imports/", blank=True, verbose_name="导入扫描XML")

    targets = models.TextField(verbose_name=u"扫描的目标集群", help_text=u"必须是IPv4格式", default="127.0.0.1")
    ports = models.ForeignKey(PortRange, verbose_name="端口范围", on_delete=models.CASCADE, related_name="task_scan_port_range", default=None)

    scan_scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, verbose_name="扫描方案", related_name="task_2_scheme")
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, verbose_name="工作组", related_name="wk_task", blank=True)

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

    def run_schedule(self):
        showed = []
        if self.atnow:
            showed.append("Run_at_now")
        if self.regular:
            showed.append("Regular: " + str(self.regular))
        if self.crontab:
            showed.append("Crontab: " + str(self.crontab))
        if self.interval:
            showed.append("Interval: " + str(self.interval))
        return "".join(showed)

    # run_schedule.admin_order_field = 'run_schedule'
    # run_schedule.short_description = '任务执行时间'

    class Meta:
        db_table = "scan_tasks"
        verbose_name = u"扫描任务"
