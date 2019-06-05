from __future__ import unicode_literals
from django.apps import AppConfig


class LocalAppConfig(AppConfig):
    name = 'services'
    verbose_name = "基础辅助服务"


    def ready(self):
        # from . import signals_handler
        return super().ready()
