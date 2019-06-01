# coding:utf-8
from __future__ import absolute_import, unicode_literals

import subprocess
import sys
import os
import django
from celery import shared_task, chain, chord
from ops.celery.decorator import register_as_period_task

# import uuid

def django_setup():
    DjangoModulePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(DjangoModulePath)
    os.chdir(DjangoModulePath)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
    django.setup()


from ops.celery.decorator import after_app_ready_start, \
    after_app_shutdown_clean_periodic, \
    register_as_period_task

# from ops.celery.Task import CustomTask
## http://docs.celeryproject.org/en/latest/userguide/configuration.html#configuration

@shared_task
def nmap_service_scan(targets="172.17.*.*"):
    django_setup()

    from scan.api.mudules.monitor.nmap_cfg import NmapScanDefaultArgs, NmapScanDefaultBin, \
        NmapDataDir, Nmap_xml_result_path
    cmds = [
        NmapScanDefaultBin
    ]
    cmds.extend(NmapScanDefaultArgs.split(" "))
    cmds.extend([targets, ])
    cmds.extend(["-oX", Nmap_xml_result_path])
    # from django.core.cache import cache
    # cache.set(__NMAP_SCAN_XML_PATH, Nmap_xml_result_path)
    try:
        p = subprocess.Popen(cmds)
        import time
        time.sleep(1)
        os.waitpid(p.pid, os.W_OK)
    except:
        import logging
        logging.error("\n>>>>>>>>>>>>>>>>>>>Nmap--ERROR----\n")
    return Nmap_xml_result_path


@shared_task
def nmap_survive_scan(targets="172.17.*.*"):
    django_setup()

    from scan.api.mudules.monitor.nmap_cfg import NmapScanDefaultArgs, NmapScanDefaultBin, \
        NmapDataDir, Nmap_xml_result_path
    cmds = [
        NmapScanDefaultBin
    ]
    cmds.extend(["-sP", "-PR", "-sn"])
    cmds.extend(["-oX", Nmap_xml_result_path])
    p = subprocess.Popen(cmds)
    import time
    time.sleep(1)
    os.waitpid(p.pid, os.W_OK)
    return Nmap_xml_result_path


@shared_task
def nmap_result_import(xml_path):
    django_setup()
    from scan.api.mudules.monitor.nmap_utils import get_needs_datas_from_xmlpath
    get_needs_datas_from_xmlpath(xml_path)
    return {
        "stat": True,
        "reason":"Nmap Scan Result Extract!"
    }


@shared_task
def push_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True)
    import time
    time.sleep(1)
    os.waitpid(p.pid, os.W_OK)
    return {
        "stat": True,
        "reason": "远程执行命令执行成功！"
    }



@shared_task
def loads_service_to_recodes(prepare=None):
    from scan.api.mudules.scan_v2.recode import collect_recodes
    collect_recodes()

    return {
        "stat": True,
        "reason": "Load All Service Prepare Recode Scan Tasks."
    }


@shared_task
def get_all_need_l2_scan_tasks(prepare=None):
    django_setup()

    from scan.models import ScanRecode
    for x in ScanRecode.objects.all():
        # print(x.script)
        result = push_cmd.delay(x.script)
        x.task_id=result.id
        x.save()

    return {
        "stat": True,
        "reason": "All OK of Tasks Scanner."
    }

@shared_task
@register_as_period_task(interval=3600*3)
def nmap_tasks(targets="192.168.2.*"):
    # chord(header=[ nmap_scan.s(), ], body=nmap_result_import.s() )()
    chain(nmap_service_scan.s(targets), nmap_result_import.s())()
    return {
        "stat": True,
        "reason": "Nmap Service Simple Scan v0.1"
    }


@shared_task
def load_cache_data(prepare=None):
    
    django_setup()
    from scan.api.mudules.monitor.nmap_utils import SURVIVE_MONITOR_CACHE_KEY
    from django.core.cache import cache
    survived_hosts = cache.get(SURVIVE_MONITOR_CACHE_KEY, [])

    return " ".join(survived_hosts)



@shared_task
@register_as_period_task(interval=3600*3)
def common_scan(targets="192.168.1.*"):
    # chord(header=[ nmap_scan.s(), ], body=nmap_result_import.s() )()
    chain(nmap_service_scan.s(targets), nmap_result_import.s(), loads_service_to_recodes.s(), get_all_need_l2_scan_tasks.s() )()
    return {"stat": True, "reason": "Scan Task End."}


@shared_task
def hosts_stat(xml_path):
    from scan.api.mudules.monitor.nmap_utils import hosts_survice_monitor
    hosts_survice_monitor(xml_path=xml_path)
    return {"stat": True, "reason": "Pushed Survive Scan Results to DB."}


@shared_task
def hosts_monitors(targets="192.168.2/0/24"):
    """
    步骤： 先进行存活扫描的检测, 再扫描对应的服务
    :param targets:
    :return:
    """

    chain(nmap_survive_scan.s(targets),
          hosts_stat.s(),
          load_cache_data.s(),
          common_scan.s())()

    return {
        "task_name": "存活性检测一条龙",
        "args": targets,
        "process": "只扫描存活的主机,而不是通用扫描。"
    }

@shared_task
@register_as_period_task(interval=3600*3)
def saved_reportstxt_2db(prepared=None):
    django_setup()

    from scan.api.mudules.scan_v2.report import txt2reportdb
    from scan.conf import REPORT_TO_SQL
    if REPORT_TO_SQL:
        txt2reportdb()

    return {
        "task_name": "ScamRecode Reports Logs 2 Db",
        "REPORT_TO_SQL": REPORT_TO_SQL,
    }
