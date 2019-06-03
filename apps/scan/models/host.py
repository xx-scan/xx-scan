import uuid
from django.db import models

from .workspace import Workspace


class Host(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    # uniq_flag = models.CharField(max_length=155, verbose_name="系统部件唯一标识", unique=True, blank=True)  ## 系统资源配置关联
    name = models.CharField(max_length=128, verbose_name=u"系统部件名称", blank=True)
    domain = models.CharField(max_length=128, verbose_name=u"域名", blank=True)
    ip = models.GenericIPAddressField(verbose_name=u'IP')
    type = models.CharField(max_length=128, verbose_name=u"系统部件的类型", default="CommonHost")
    os = models.CharField(max_length=128, verbose_name=u"操作系统", default="Linux")
    mac = models.CharField(max_length=128, verbose_name=u"mac地址", blank=True)
    mac_vendor = models.CharField(max_length=128, verbose_name=u"厂家", blank=True)
    up = models.BooleanField(verbose_name="存活状态", default=True)
    extra = models.TextField(verbose_name=u"额外补充信息", default="")
    comment = models.TextField(verbose_name=u"系统部件描述", default="-")
    # managers = models.ManyToManyField("ConnectManagerUserInfo", related_name="sys_cop_conn_users")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # 2019-6-1
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="workspace_hosts")

    class Meta:
        db_table = "hosts"
        verbose_name = "主机设备表"


class Service(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="host_service")
    port = models.CharField(max_length=7, verbose_name=u"端口", blank=True)
    hostname = models.CharField(max_length=55, verbose_name=u"主机名", blank=True)
    banner = models.CharField(max_length=155, verbose_name=u"产品", blank=True)
    protocol = models.CharField(max_length=255, verbose_name=u"协议", blank=True)
    state = models.CharField(max_length=255, verbose_name=u"状态", blank=True)
    service = models.CharField(max_length=255, verbose_name=u"服务", blank=True)
    version = models.CharField(max_length=255, verbose_name=u"版本", blank=True)
    reason = models.CharField(max_length=255, verbose_name=u"反馈原因", blank=True)
    descover_time = models.DateTimeField(verbose_name="发现时间")

    running = models.BooleanField(verbose_name="运行中", default=True)

    class Meta:
        db_table="host_services"
        verbose_name="主机服务探测"