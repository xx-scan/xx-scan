from django.db import models


## 操作历史记录
class PlatOptHistory(models.Model):
    # host = models.CharField(u"主机URL", default="http://localhost:80")
    desc = models.CharField(u"操作描述", max_length=155, default="")
    type = models.CharField(u"操作类型", max_length=155, default="平台日志")
    extra = models.CharField(u"备用字段", max_length=155, default="")
    opreatername = models.CharField(u"操作者", max_length=55, default="actanble")
    opreate_time = models.DateTimeField(u"添加时间", auto_now=True, editable=False)
    conn_file = models.CharField(u"关联文件", max_length=255, default="")
    remote_file = models.CharField(u"远程文件", max_length=255, default="")

    class Meta:
        verbose_name = u"操作历史记录"
        ordering = ["-opreate_time"]


