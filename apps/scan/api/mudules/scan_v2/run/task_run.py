# coding:utf-8
from celery import chain, chord

from ops.celery.utils import create_or_update_celery_periodic_tasks

from scan.tasks import nmap_result_import, loads_service_to_recodes , run_all_level2_scan_tasks


def descover_run(targets, ports, scheme, domains=None):

    pass



def import_run(import_file, scheme, workspace):
    # from scan.api.mudules.monitor.nmap_utils import get_needs_datas_from_xmlpath


    chain(nmap_result_import.s(xml_path=import_file, workspaceid=workspace),

          loads_service_to_recodes.s(),
          run_all_level2_scan_tasks.s()


          )

    pass


def run(scantask):
    ## 当前都是立即执行的;

    if scantask.imports_active:
        import_run(scantask.import_file, scheme=scantask.scan_scheme, workspace=scantask.workspace)
        return

    descover_run(scantask.targets, scantask.ports, scantask.scan_scheme)

