# nginx 和 opt 日志下面必须有目录

## mkdir -p /var/log/nginx/cache/test_env
## mkdir -p /var/log/supervisor
## mkdir -p /opt/ ## 相关文件必须备份的外部文件


## 2019-3-19
- 修改和删除msg

```python 

from django.db import models

## 平台消息的初始视图
class MsgStat(models.Model):
    ## 关联的审计日志的ID
    audit_logid = models.CharField(u"告警日志标号", max_length=155, default="")
    # is_show = models.BooleanField(u"是否展示", default=True)
    solved = models.BooleanField(u"解决状态", default=False)
    opreate_time = models.DateTimeField(u"添加时间", auto_now=True, editable=False)
    opreate_username = models.CharField(u"操作者", max_length=55, default="waf001")
    # idea = models.CharField(u"处理说明", max_length=155, default="")
    # stat = models.IntegerField(u"处理状态", default=0)

    def viewd(self):
        self.solved = True

    class Meta:
        verbose_name = u"平台消息状态"
        db_table = "msgstat"
```