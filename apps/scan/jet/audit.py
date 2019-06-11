import uuid
from django.db import models


class PlatAlertAudit(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(verbose_name="日志内容描述", max_length=255, default="-")
    content = models.CharField(verbose_name="内容", max_length=255, default="-")
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "plat_alert"
        verbose_name = "告警"


## 2019-6-10
# 当前记录的内容为平台中存在没有注册的2阶段扫描服务，这里进行记录。

## 2019-6-11
# 舍弃, 用 Service 的 PlatHistory 代替