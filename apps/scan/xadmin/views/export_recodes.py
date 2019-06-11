import os, re
from scan.models import ScanRecode, ScanReport
import xadmin
from xadmin.views import ModelAdminView
from xadmin.views import BaseAdminView
from django.http import HttpResponse, HttpResponseRedirect

def exports_recodes():
    """
    ## 这里只涉及到文件导出到Report 后续有压缩包导出
    :return:
    """
    srid_lists = []
    for x in ScanRecode.objects.filter(exported=False):

        matched = re.match(".*?(/home/django.*?\.txt).*", x.script)
        if not matched:
            continue

        _filepath = matched.group(1)

        if not os.path.exists(_filepath):
            print(_filepath)
            try:
                from services.models import PlatOptHistory
                PlatOptHistory.objects.create(
                    extra="脚本执行错误;",
                    desc=str(str(x.id) + "[" + x.script + "]")
                )
            except:
                import logging
                logging.error(x.script + "<<<- Error, Not This Bin!")
            continue

        with open(_filepath, "r", encoding="utf-8") as f:
            txt = f.read()
            f.close()
        srid_lists.append(x.id)

        ScanReport.objects.create(scan_recode=x, report=txt)

    ScanRecode.objects.filter(id__in=srid_lists).update(exported=True)



class RecodeExportView(BaseAdminView):

    def get(self, request):
        exports_recodes()
        return HttpResponseRedirect("/scan/scanreport/")


xadmin.site.register_view(r'^recode_export/$', RecodeExportView, name='exports_recodes')

