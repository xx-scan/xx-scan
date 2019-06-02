import uuid
from django.db import models

import os

from website.settings import PROJECT_DIR
RESULT_PATH = os.path.join(PROJECT_DIR, "results")


class Protocol(models.Model):
    protocol = models.CharField(max_length=55, verbose_name=u"协议", unique=True, db_index=True)

    def __str__(self):
        return self.protocol

    class Meta:
        db_table = "protocols"
        verbose_name = "协议组"


# 独立出去的扫描服务映射关系
class NmapServiceName(models.Model):
    protocol = models.ForeignKey(Protocol, verbose_name="针对协议",
         related_name="nmap_service_protocol", on_delete=models.DO_NOTHING, blank=True)
    #service_name = models.CharField(max_length=255, verbose_name=u"模糊协议", unique=True)
    service_name = models.CharField(max_length=255, verbose_name=u"服务名", unique=True)
    active = models.BooleanField(verbose_name="激活.当前有工具的状态", default=True)

    def __str__(self):
        return str(self.service_name) + "[" + str(self.protocol) + "]"

    class Meta:
        db_table = "nmap_service_names"
        verbose_name = "协议对照表"


class ScanTool(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=55, verbose_name=u"扫描器英文名称", blank=True)
    protocol = models.ForeignKey(Protocol, verbose_name="针对协议",
         related_name="scan_protocol", on_delete=models.DO_NOTHING, blank=True)
    used_script = models.TextField(verbose_name=u"使用命令", default="")
    args = models.CharField(verbose_name=u"需要准备的参数集合", max_length=100, default="", help_text="扫描参数-h")
    extra = models.TextField(verbose_name=u"额外补充信息", default="")
    comment = models.TextField(verbose_name=u"扫描器设定描述", default="")

    def save(self, *args, **kwargs):
        try:
            import re
            matched = re.match('^(.*?)\s.*', self.used_script)
            if matched:
                self.name = matched.group(1).split("/")[-1]
            else:
                self.name = self.id
            super(ScanTool, self).save(*args, **kwargs)
        finally:
            pass

    def __str__(self):
        return str(self.protocol) + "["+ self.name +"]"

    class Meta:
        db_table = "scan_tools"
        verbose_name = "扫描工具集合"


class ScanRecode(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    scan_tool = models.ForeignKey(ScanTool, verbose_name="使用的扫描工具", on_delete=models.CASCADE, related_name="scan_event_2_scan_tool" )
    target = models.GenericIPAddressField(verbose_name="扫描的IP目标")
    port = models.IntegerField(verbose_name="扫描端口")
    path = models.CharField(verbose_name="PATH路径", blank=True, max_length=255)
    output = models.CharField(max_length=255, verbose_name=u"保存路径", blank=True)
    task_id = models.CharField(max_length=155, verbose_name=u"任务ID", blank=True)
    # managers = models.ManyToManyField("ConnectManagerUserInfo", related_name="sys_cop_conn_users")
    script = models.TextField(verbose_name="完整的执行脚本", blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def extract_self(self):
        from datetime import datetime
        _date = str(datetime.now().date()).replace("-", "")

        output = self.scan_tool.name + "-" \
                 + self.target + "-" \
                 + self.port + "-" \
                 + _date  if not self.output else str(uuid.uuid4())


        OutputDir = os.path.join(RESULT_PATH, self.target + "-" + str(self.port))
        if not os.path.exists(OutputDir):
            os.makedirs(OutputDir)
        # self.output = str(os.path.join(OutputDir, output))
        _path = os.path.join(OutputDir, output)
        script = self.scan_tool.used_script.replace("[TARGET]", self.target
                                        ).replace( "[PORT]", str(self.port)
                                        ).replace("[OUTPUT]", _path
                                        ).replace("[PATH]", self.path)
        return output, script

    def save(self, *args, **kwargs):
        try:
            output, script = self.extract_self()
            self.output = output
            self.script = script
            super(ScanRecode, self).save(*args, **kwargs)
        finally:
            pass

    class Meta:
        db_table = "scan_recode"
        verbose_name = "扫描事件"


# 定制扫描器的扫描方案
class Scheme(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(verbose_name="方案名称", blank=True, max_length=100)
    desc = models.TextField(verbose_name="方案描述", blank=True)

    scan_tools = models.ManyToManyField(ScanTool, related_name="scan_tools_2_scheme", blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "scan_scheme"
        verbose_name = "扫描方案"