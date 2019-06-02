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
def nmap_scan(targets="172.17.*.*"):
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
def nmap_result_import(xml_path):
    django_setup()

    from scan.api.mudules.monitor.nmap_utils import get_needs_datas_from_xmlpath
    try:
        # from django.core.cache import cache
        # _path = cache.get(__NMAP_SCAN_XML_PATH)
        get_needs_datas_from_xmlpath(xml_path)
    except Exception as e:
        import logging
        logging.error("\n>>>>Extract Error---\n")
    return "Nmap Scan Result Extract!"


@shared_task
def push_cmd(cmd):
    try:
        p = subprocess.Popen(cmd, shell=True)
        import time
        time.sleep(1)
        os.waitpid(p.pid, os.W_OK)
    except:
        print("\n>>>>>>>>>>>>>>>>>>>Nmap--ERROR----\n")
    return "Task OK"


@shared_task
def loads_service_to_recodes(prepare=None):
    from scan.api.mudules.scan_v2.recode import collect_recodes
    collect_recodes()

    return "Load Recode End."


@shared_task
def get_all_need_l2_scan_tasks(prepare=None):
    django_setup()

    from scan.models import ScanRecode
    for x in ScanRecode.objects.all():
        print(x.script)
        result = push_cmd.delay(x.script)
        x.task_id=result.id
        x.save()

    return "all_ok"

@shared_task
@register_as_period_task(interval=3600*3)
def nmap_tasks(targets="192.168.2.*"):
    # chord(header=[ nmap_scan.s(), ], body=nmap_result_import.s() )()
    chain(nmap_scan.s(targets), nmap_result_import.s())()
    return "Task End"


@shared_task
@register_as_period_task(interval=3600*3)
def chain_all_tasks(targets="192.168.1.*"):
    # chord(header=[ nmap_scan.s(), ], body=nmap_result_import.s() )()
    chain(nmap_scan.s(targets), nmap_result_import.s(), loads_service_to_recodes.s(), get_all_need_l2_scan_tasks.s() )()
    return "Task End"

"""
from scan.tasks import chain_all_tasks
chain_all_tasks().delay("192.168.1.*")
"""