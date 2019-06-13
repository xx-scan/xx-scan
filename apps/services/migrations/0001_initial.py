# Generated by Django 2.1.7 on 2019-06-09 17:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PlatOptHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(default='', max_length=155, verbose_name='操作描述')),
                ('type', models.CharField(default='平台日志', max_length=155, verbose_name='操作类型')),
                ('extra', models.CharField(default='', max_length=155, verbose_name='备用字段')),
                ('opreatername', models.CharField(default='actanble', max_length=55, verbose_name='操作者')),
                ('opreate_time', models.DateTimeField(auto_now=True, verbose_name='添加时间')),
                ('conn_file', models.CharField(default='', max_length=255, verbose_name='关联文件')),
                ('remote_file', models.CharField(default='', max_length=255, verbose_name='远程文件')),
            ],
            options={
                'verbose_name': '操作历史记录',
                'ordering': ['-opreate_time'],
            },
        ),
        migrations.CreateModel(
            name='UserAuditLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(default='/waf/mg/jwt_login/', max_length=255, verbose_name='请求URL')),
                ('request_method', models.CharField(default='POST', max_length=255, verbose_name='请求方法')),
                ('ip', models.GenericIPAddressField(default='0.0.0.0', verbose_name='IP')),
                ('username', models.CharField(max_length=255, verbose_name='访问的用户的用户名')),
                ('status', models.CharField(choices=[('200', '正常'), ('400', '请求错误'), ('403', '访问阻断'), ('401', '认证失败')], default='200', max_length=5, verbose_name='请求状态')),
                ('opreate_time', models.DateTimeField(auto_now=True, verbose_name='操作时间')),
                ('param', models.CharField(default='', max_length=255, verbose_name='参数')),
            ],
            options={
                'verbose_name': '审计用户操作',
                'db_table': 'user_auditlog',
                'ordering': ['-opreate_time'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(default='描述', max_length=255, verbose_name='请求URL')),
                ('truename', models.CharField(default='真实姓名', max_length=55, verbose_name='真实名字')),
                ('_private_key', models.TextField(blank=True, max_length=4096, null=True, verbose_name='SSH private key')),
                ('_public_key', models.TextField(blank=True, max_length=4096, verbose_name='SSH public key')),
                ('identity', models.CharField(choices=[('NetworkManager', '安全管理员'), ('DbUser', '审计员'), ('SuperManager', '管理员')], default='Guest', max_length=50)),
                ('passwd', models.CharField(default='1q2w3e4r', max_length=55, verbose_name='明文密码')),
                ('remarks', models.CharField(default='Guest', max_length=55, verbose_name='备注')),
                ('extra', models.CharField(default='无备注描述', max_length=155, verbose_name='备用字段')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waf', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '用户信息',
                'db_table': 'userprofile',
            },
        ),
    ]
