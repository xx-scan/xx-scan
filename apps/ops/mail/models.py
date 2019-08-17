from django.db import models
import uuid

from ops.logging import MailLoger
from ops.libs.opssdk.operate.mail import Mail


class MailHost(models.Model):
    id = models.UUIDField(default=uuid.uuid4, verbose_name='ID', primary_key=True)
    mail_host = models.CharField(verbose_name=u"邮件服务端地址", max_length=255, help_text='邮件服务端地址例如smtp.163.com', default='smtp.163.com')
    mail_user = models.CharField(verbose_name=u"邮件用户名", max_length=255, help_text='邮件用户名root')
    mail_pass = models.CharField(verbose_name=u"邮件用户名", max_length=255, help_text='邮件设置的棉麻')
    mail_postfix = models.CharField(verbose_name=u"邮件后缀", max_length=255, help_text='邮件用户名root', default='163.com')
    default_recv = models.CharField(verbose_name=u"默认接收者", max_length=255, default='180573956@qq.com,admin@actanble.com')
    active = models.BooleanField(verbose_name=u"生效", default=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='审计时间')

    def to_dict(self):
        return dict(mail_host=self.mail_host, mail_user=self.mail_user, mail_pass=self.mail_pass, mail_postfix=self.mail_postfix)

    class Meta:
        db_table = "mail_hosts"
        verbose_name = "邮件服务端列表"
        ordering = ('active', '-date_created', )


from .setttings import DEFAULT_RECEIVED_LIST


class MailAudit(models.Model):
    id = models.UUIDField(default=uuid.uuid4, verbose_name='ID', primary_key=True)
    mail_host = models.ForeignKey(MailHost, related_name='mail_host_audits', verbose_name='Mail Host', blank=True, on_delete=models.CASCADE)
    to_list = models.TextField(verbose_name='收件的邮件列表', default=DEFAULT_RECEIVED_LIST)
    header = models.CharField(verbose_name='发送邮件显示名称', default='CSO管理平台', max_length=50)
    sub = models.CharField(verbose_name='发送邮件的标题', default='告警', max_length=200)
    content = models.TextField(verbose_name='邮件内容', default='空')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')

    def to_dict(self):
        return dict(
            to_list=self.to_list, header=self.header, sub=self.sub, content=self.content, subtype='plain', att='none'
        )

    def save(self, *args, **kwargs):
        self.mail_host = MailHost.objects.filter(active=True).order_by('-date_created')[0]
        try:
            Mail(**self.mail_host.to_dict()).send_mail(**self.to_dict())
        except:
            MailLoger.error('执行邮件发送错误')
        MailLoger.info('发送邮件成功！' + self.sub)
        super(MailAudit, self).save(*args, **kwargs)

    class Meta:
        db_table = "mail_audits"
        verbose_name = "邮件发送审计"
        ordering = ('-date_created',)

