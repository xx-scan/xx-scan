# coding:utf-8

import uuid
from django.db import models
from django.contrib.auth.models import User


class Workspace(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="工作台用户", related_name="user_workspace", blank=True)
    name = models.CharField(verbose_name="空间名称", max_length=55, help_text="空间名称推荐英文")

    # desc = models.TextField(verbose_name="描述", help_text="描述", blank=True)
    summary = models.TextField(verbose_name="空间简介", blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + "[" + self.user.username + "]"

    # def save(self, *args, **kwargs):
    #     try:
    #         print(self)
    #         print(args)
    #         print(kwargs)
    #     finally:
    #         pass

    class Meta:
        db_table = "workspace"
        verbose_name = "用户空间"