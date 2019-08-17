from .models import CronConfig


class Crontab:

    def __init__(self, cron):
        self.cron = cron

    def obj(self, save=False):
        cron_minute, cron_hour, cron_day, cron_month, cron_week = self.cron.split()
        cron_name = self.cron
        cron_cfg_obj = CronConfig(**locals())
        if save:
            cron_cfg_obj.save()
        return cron_cfg_obj


class Interval:

    def __init__(self, second=None, minute=None, hour=None):
        self.second = second
        self.minute = minute
        self.hour = hour

    def obj(self, save=False):
        if self.second:
            obj = CronConfig(cron_second="*/{}".format(self.second),
                              cron_name="every {} minute".format(str(self.second)))

        if self.minute:
            obj =  CronConfig(cron_second='0', cron_minute='*/{}',
                              cron_name="every {} minute".format(str(self.minute)))

        if self.hour:
            obj = CronConfig(cron_second='0', cron_minute='0', cron_hour='*/{}',
                              cron_name="every {} hour".format(str(self.hour)))
        else:
            raise AttributeError("Interval类型只支持时分秒的扩展。")

        if save:
            obj.save()
