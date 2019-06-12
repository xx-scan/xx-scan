import os, re
from django.db import DatabaseError, transaction
from django.http import HttpResponse, HttpResponseRedirect

import xadmin
from xadmin.views import BaseAdminView

from scan.models import ScanRecode, ScanReport

def exports_recodes(user=None):
    """
    ## 这里只涉及到文件导出到Report 后续有压缩包导出
    :return:
    """
    recodes = ScanRecode.objects.all()
    for x in recodes:
        x.export2txt()

## 2019-6-1
# ScanRecode 进行Update Save过程中进行这个函数。
def export_recode_2_report(recode):
    matched = re.match(".*?(/home/django.*?\.txt).*", recode.script)
    if not matched:
        return None

    _filepath = matched.group(1)
    if not os.path.exists(_filepath):
        try:
            from services.models import PlatOptHistory
            PlatOptHistory.objects.create(
                extra="脚本执行错误;",
                desc=str(recode.id) + "[" + recode.script + "]"
            )
        except:
            import logging
            logging.error(recode.script + "<<<- Error, Not This Bin!")
        return None

    with open(_filepath, "r", encoding="utf-8") as f:
        txt = f.read()
        f.close()

    recode.exported = True

    try:
        with transaction.atomic():
            #transaction.commit()
            recode.save()
    except DatabaseError:
        recode.exported = False
        from scan.utils.ltool.utils.logaudit import put_log
        put_log(type="脚本日志",
                desc="Django Model原子事务错误。",
                extra=str(recode.script))

    obj = ScanReport(scan_recode=recode, report=txt)
    try:
        with transaction.atomic():
            #transaction.commit()
            obj.save()
    except DatabaseError:
        from scan.utils.ltool.utils.logaudit import put_log
        put_log(type="脚本日志",
                desc="Django Model原子事务错误。",
                extra="关联到ScanReport")


class RecodeExportView(BaseAdminView):

    def get(self, request):
        exports_recodes(user=request.user)
        return HttpResponseRedirect("/scan/scanreport/")


xadmin.site.register_view(r'^recode_export/$', RecodeExportView, name='exports_recodes')

