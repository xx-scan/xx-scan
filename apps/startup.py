#!/usr/bin/env python
# -*-coding:utf-8-*-
import fire
from tornado.options import define
from ops.libs.websdk.program import MainProgram
from website.tor_settings import settings as app_settings
from ops.apscheduler.handler import Application as CronApp


define("service", default='web', help="start service flag", type=str)


class MyProgram(MainProgram):
    def __init__(self, service='cron', progress_id='cron_tasks'):
        self.__app = None
        settings = app_settings

        if service == "cron":
            self.__app = CronApp(**settings)

        super(MyProgram, self).__init__(progress_id)
        self.__app.start_server()


if __name__ == '__main__':
    fire.Fire(MyProgram)

