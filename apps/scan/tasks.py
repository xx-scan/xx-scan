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

django_setup()

from ops.celery.decorator import after_app_ready_start, \
    after_app_shutdown_clean_periodic, \
    register_as_period_task

# from ops.celery.Task import CustomTask
## http://docs.celeryproject.org/en/latest/userguide/configuration.html#configuration

@shared_task
def nmap_service_scan(targets="172.17.*.*", workspaceid=None):


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


    from scan.api.mudules.monitor.nmap_cfg import NmapScanDefaultArgs, NmapScanDefaultBin, \
        NmapDataDir, Nmap_xml_result_path
    cmds = [
        NmapScanDefaultBin
    ]
    cmds.extend(["-sP", "-PR", "-sn", targets])
    cmds.extend(["-oX", Nmap_xml_result_path])
    p = subprocess.Popen(cmds)
    import time
    time.sleep(1)
    os.waitpid(p.pid, os.W_OK)
    return Nmap_xml_result_path


@shared_task
def nmap_result_import(xml_path, workspaceid):


    from scan.models import Workspace
    from scan.api.mudules.monitor.nmap_utils import get_needs_datas_from_xmlpath
    get_needs_datas_from_xmlpath(xml_path, workspace=Workspace.objects.get(id=workspaceid))
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
def run_all_level2_scan_tasks(prepare=None):
    """
    开始执行第二个扫描阶段需要执行的内容
    :param prepare:
    :return:
    """
    from scan.models import ScanRecode
    for x in ScanRecode.objects.filter(active=True):
        # print(x.script)
        result = push_cmd.delay(x.script)
        x.task_id=result.id
        x.save()

    return {
        "stat": True,
        "reason": "All OK of Tasks Scanner."
    }


@shared_task
def load_cache_data(prepare=None):

    from scan.api.mudules.monitor.nmap_utils import SURVIVE_MONITOR_CACHE_KEY
    from django.core.cache import cache
    survived_hosts = cache.get(SURVIVE_MONITOR_CACHE_KEY, [])

    return " ".join(survived_hosts)


@shared_task
@register_as_period_task(interval=3600*3)
def common_scan(workspace=None, targets="192.168.1.*"):
    # chord(header=[ nmap_scan.s(), ], body=nmap_result_import.s() )()
    chain(nmap_service_scan.s(targets),
          nmap_result_import.s(),
          loads_service_to_recodes.s(),
          run_all_level2_scan_tasks.s() )()
    return {"stat": True, "reason": "Scan Task End."}
