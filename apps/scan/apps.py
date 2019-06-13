from __future__ import unicode_literals
from django.apps import AppConfig


class LocalAppConfig(AppConfig):
    name = 'scan'
    verbose_name = "扫描器管理"
    orderIndex_ = 10

    def ready(self):
        # from . import signals_handler
        return super().ready()
