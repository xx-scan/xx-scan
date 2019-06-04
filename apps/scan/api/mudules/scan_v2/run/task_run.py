# coding:utf-8
from celery import chain, chord

from ops.celery.utils import create_or_update_celery_periodic_tasks
from scan.models import ScanTask


def descover_run(scantaskid):
    from scan.tasks import nmap_result_import, recodes_and_run, nmap_service_scan
    chain(nmap_service_scan.s(scantaskid),
        nmap_result_import.s(),
          recodes_and_run.s())()
    return "Common Scan"


def import_run(xml_path, workspaceid, scan_schemeid):
    from scan.tasks import nmap_result_import, recodes_and_run

    chain(nmap_result_import.s([xml_path, workspaceid, scan_schemeid]),
          recodes_and_run.s())()

    return "Import Scan"



