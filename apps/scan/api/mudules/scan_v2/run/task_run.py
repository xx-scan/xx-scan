# coding:utf-8
from celery import chain, chord

from ops.celery.utils import create_or_update_celery_periodic_tasks
from scan.models import ScanTask


def descover_run(scantaskid):
    from scan.tasks import nmap_result_import, recodes_and_run, nmap_tcp_scan, nmap_udp_scan
    scan_task = ScanTask.objects.get(id=scantaskid)
    if scan_task.udp:
        chain(nmap_udp_scan.s(scantaskid),
            nmap_result_import.s(),
              recodes_and_run.s())()
        return "Udp Scan"

    chain(nmap_tcp_scan.s(scantaskid),
          nmap_result_import.s(),
          recodes_and_run.s())()
    return "Tcp Fast Scan"


def import_run(xml_path, workspaceid, scan_schemeid):
    from scan.tasks import nmap_result_import, recodes_and_run

    chain(nmap_result_import.s([xml_path, workspaceid, scan_schemeid]),
          recodes_and_run.s())()

    return "Xml Import Scan"



