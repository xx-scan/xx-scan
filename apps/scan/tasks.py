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
from scan.models import Workspace, ScanTask

@shared_task
def push_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True)
    import time
    time.sleep(1)
    os.waitpid(p.pid, os.W_OK)
    return {
        "stat": True,
        "cmd": cmd,
        "reason": "远程执行命令执行成功！"
    }

from ops.celery.decorator import after_app_ready_start, \
    after_app_shutdown_clean_periodic, \
    register_as_period_task

# from ops.celery.Task import CustomTask
## http://docs.celeryproject.org/en/latest/userguide/configuration.html#configuration


def nmap_scan(nmap_args, scantaskid):
    from scan.api.mudules.monitor.nmap_cfg import NmapScanDefaultBin, \
        NmapDataDir, Nmap_xml_result_path

    scantask = ScanTask.objects.get(id=scantaskid)
    ports = scantask.ports.ports
    targets = scantask.targets

    cmds = [
        NmapScanDefaultBin
    ]
    cmds.extend("{nmap_args} -p{ports} -O".format(ports=ports, nmap_args=nmap_args).split(" "))
    cmds.extend([targets, ])
    cmds.extend(["-oX", Nmap_xml_result_path])
    # from django.core.cache import cache
    # cache.set(__NMAP_SCAN_XML_PATH, Nmap_xml_result_path)

    # 2019-6-5 修改这个地方， 一旦失败跳出来。而不是用try
    p = subprocess.Popen(cmds)
    import time
    time.sleep(1)
    os.waitpid(p.pid, os.W_OK)

    return [Nmap_xml_result_path, scantask.workspace.id, scantask.scan_scheme.id]


@shared_task
def nmap_tcp_scan(scantaskid):
    return nmap_scan(nmap_args="-sS -sV", scantaskid=scantaskid)


@shared_task
def nmap_udp_scan(scantaskid):
    return nmap_scan(nmap_args="-sU -sV", scantaskid=scantaskid)


# 上面是存活检测; 存活检测之后，缩小主机范围再扫描。但是不准确一般来说。
# 存活检测目前是测试阶段，存活检测的规则是 nmap -sP 不完整。
@shared_task
def nmap_survive_scan(scantaskid):
    # 这里是基于UCP扫描的Scan
    return nmap_scan(nmap_args="-sU -T5 -sV --max-retries 1", scantaskid=scantaskid)


@shared_task
def nmap_result_import(args):
    xml_path, workspaceid, scan_schemeid = args[0], args[1], args[2]
    from scan.api.mudules.monitor.nmap_utils import get_needs_datas_from_xmlpath
    get_needs_datas_from_xmlpath(xml_path, workspaceid=workspaceid)
    return [workspaceid, scan_schemeid]

# =================================================================
# 2019-6-4 晚上 21：11 记录：这个地方实际上执行非常快，为社么要分开。
# 原因 后面不一定是调用nmap扫描出来的结果，也可能是 Masscan, Nessus, Nexpose 等等，都能进行格式化，充值任务。
# =================================================================


@shared_task
def recodes_and_run(args):
    workspaceid, scan_schemeid = args[0], args[1]
    from scan.api.mudules.scan_v2.recode import collect_recodes
    runed_scripts = []

    recodes = collect_recodes(scheme_id=scan_schemeid, workspaceid=workspaceid)
    for x in recodes:
        result = push_cmd.delay(x.script)
        runed_scripts.append(x.script)
        x.task_id=result.id
        # 在这个环节可以把task_id都存下来便于下次
        x.save()
    return {
        "scripts_num": len(runed_scripts),
        "scripts": runed_scripts,
        "stat": True,
        "reason": "All OK of Tasks Scanner.",
        "workspaceid": workspaceid
    }


@shared_task
def run(scantaskid):
    from scan.api.mudules.scan_v2.run.task_run import import_run, descover_run
    import time
    time.sleep(2)
    ## 当前都是立即执行的;
    scantask = ScanTask.objects.get(id=scantaskid)
    if scantask.imports_active:
        return import_run(str(scantask.imports.path),
                          workspaceid=scantask.workspace.id,
                        scan_schemeid=scantask.scan_scheme.id)
    return descover_run(scantaskid)