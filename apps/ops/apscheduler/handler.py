#!/usr/bin/env python
# -*-coding:utf-8-*-

import time, datetime
import json
from dateutil.relativedelta import relativedelta
from ops.libs.websdk.application import Application as myApp
from ops.apscheduler.cron import cron_jobs
from ops.libs.websdk.web_logs import ins_log
from ops.libs.websdk.base_handler import LivenessProbe
# from apscheduler.schedulers.tornado import TornadoScheduler
from ops.libs.base_handler import BaseHandler
from ops.apscheduler.cron.models import CronLog
from tornado.options import options
from django.forms.models import model_to_dict
# from django.db.models import Q

from ops.apscheduler.aps_helper import get_mysql_jobstores, get_django_scheduler
scheduler = get_django_scheduler()


def job_from(**jobargs):
    """
    :param jobargs: job 参数包括 cron params job_id args
    :return:
    """
    job_id = jobargs['job_id']
    func = getattr(cron_jobs, 'exec_task')
    args = jobargs['params']
    cron = jobargs['cron'].split(' ')
    cron_rel = dict(second=cron[0], minute=cron[1], hour=cron[2], day=cron[3], month=cron[4], day_of_week=cron[5])
    scheduler.add_job(func=func, id=job_id, kwargs={'params': args, 'job_id': job_id}, trigger='cron', **cron_rel,
                      replace_existing=True)
    return job_id


class CronJobs(BaseHandler):
    def get(self, *args, **kwargs):
        page_size = self.get_argument('page', default=1, strip=True)
        limit = self.get_argument('limit', default=15, strip=True)
        job_id = self.get_argument('job_id', default=None, strip=True)

        limit_start = (int(page_size) - 1) * int(limit)
        limit_end = int(page_size) * int(limit)
        info_list = []
        try:
            if not job_id:
                ret_list = scheduler.get_jobs()
            else:
                ret_list = [scheduler.get_job(job_id)]
                limit_start = 0
            for ret in ret_list:
                fields = ret.trigger.fields
                cron = {}
                for field in fields:
                    cron[field.name] = str(field)
                info = {
                    'job_id': ret.id,
                    'next_run_time': str(ret.next_run_time),
                    'run_params': ret.kwargs.get('params'),
                    'status': '0' if ret.next_run_time else '1',
                    'cron1': cron,
                    'cron': cron.get("second") + " " + cron.get("minute") + " " + cron.get("hour") + " " + cron.get(
                        "day") + " " + cron.get("month") + " " + cron.get("day_of_week")
                }
                info_list.append(info)

            return self.write(dict(code=0, msg='获取成功', data=info_list[limit_start:limit_end], count=len(info_list)))
        except Exception as e:
            return self.write(dict(code=-1, msg="错误 " + str(e)))

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        if len(data.get('cron').strip().split(' ')) != 6:
            return self.write(dict(code=-1, msg='添加失败，定时器错误'))
        # print(data)
        job = job_from(**data)
        return self.write(dict(code=0, msg='添加成功', job_id=job))

    def put(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        if len(data.get('cron').strip().split(' ')) != 6:
            return self.write(dict(code=-1, msg='修改失败，定时器错误'))
        job_id = data.get('job_id')
        try:
            old_job = scheduler.get_job(job_id)
            if old_job:
                job_from(**data)
                response = dict(code=0, msg="job {} edit success!".format(job_id))
            else:
                response = dict(code=-1, msg="job {} Not Found!".format(job_id))
        except Exception as e:
            response = dict(code=-2, msg=str(e))
        return self.write(response)

    def delete(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        job_id = data.get('job_id')
        if not job_id:
            return self.write(dict(code=-1, msg='job id 不能为空'))
        scheduler.remove_job(job_id)
        return self.write(dict(code=0, msg='删除成功', job_id=job_id))

    def patch(self, *args, **kwargs):
        """暂停作业/恢复作业"""
        data = json.loads(self.request.body.decode("utf-8"))
        job_id = data.get('job_id')
        if not job_id:
            return self.write(dict(code=-1, msg='job id 不能为空'))
        if scheduler.get_job(job_id).next_run_time:
            control = 'pause'
        else:
            control = 'resume'

        if control == 'pause':
            try:
                scheduler.pause_job(job_id)
                response = dict(code=0 ,msg="job {} 禁用执行成功！" .format(job_id))
            except Exception as e:
                response = dict(code=-2, msg="job {} {}".format(job_id,str(e)))
            return self.write(response)
        elif control == 'resume':
            try:
                scheduler.resume_job(job_id)
                response = dict(code=0, msg="job {} 恢复执行成功".format(job_id))
            except Exception as e:
                response = dict(code=-3, msg="job {} {}".format(job_id, str(e)))
            return self.write(response)
        return self.write(dict(code=-4, msg='失败了'))


class CronLogs(BaseHandler):

    def get(self, *args, **kwargs):
        page_size = self.get_argument('page', default=1, strip=True)
        limit = self.get_argument('limit', default=10, strip=True)
        key = self.get_argument('key', default=None, strip=True)
        value = self.get_argument('value', default=None, strip=True)
        start_date = self.get_argument('start_date', default=None, strip=True)
        end_date = self.get_argument('end_date', default=None, strip=True)
        limit_start = (int(page_size) - 1) * int(limit)

        if not start_date:
            start_date = datetime.date.today() - relativedelta(months=+1)
        if not end_date:
            end_date = datetime.date.today() + datetime.timedelta(days=1)

        # start_time_tuple = time.strptime(str(start_date), '%Y-%m-%d')
        # end_time_tuple = time.strptime(str(end_date), '%Y-%m-%d')
        log_list = []

        if key and value:
            count = CronLog.objects.filter(exec_time__gt=start_date, exec_time__lt=end_date).filter(**{key: value}).count()
            log_info = CronLog.objects.filter(exec_time__gt=start_date, exec_time__lt=end_date
                            ).filter(**{key: value}).order_by('-exec_time')[limit_start: limit_start+limit]
        else:
            count = CronLog.objects.filter(exec_time__gt=start_date, exec_time__lt=end_date).count()
            log_info = CronLog.objects.filter(exec_time__gt=start_date,
                  exec_time__lt=end_date).order_by('-exec_time')[limit_start: limit_start+limit]

        for msg in log_info:
            data_dict = model_to_dict(msg)
            data_dict['exec_time'] = msg.exec_time.strftime("%Y-%m-%d %H:%M:%S")
            log_list.append(data_dict)

        return self.write(dict(code=0, status=0, msg='获取成功', count=count, data=log_list))


class Application(myApp):
    def __init__(self, **settings):
        self.__settings = settings
        urls = []
        urls.extend(cron_urls)
        super(Application, self).__init__(urls, **settings)

    def start_server(self):
        """
        启动 tornado 服务
        :return:
        """
        try:
            ins_log.read_log('info', 'progressid: %(progid)s' % dict(progid=options.progid))
            ins_log.read_log('info', 'server address: %(addr)s:%(port)d' % dict(addr=options.addr, port=options.port))
            ins_log.read_log('info', 'web server start sucessfuled.')
            scheduler.start()
            self.io_loop.start()
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown(wait=True)
            self.io_loop.stop()
        except:
            import traceback
            ins_log.read_log('error', '%(tra)s' % dict(tra=traceback.format_exc()))


cron_urls = [
    (r"/v1/cron/job/", CronJobs),
    (r"/v1/cron/log/", CronLogs),
    (r"/are_you_ok/", LivenessProbe),
]

if __name__ == '__main__':
    pass
