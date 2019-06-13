# coding:utf-8
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from django.http import StreamingHttpResponse, HttpResponse

from ....models import ScanRecode, ScanReport


def txt2reportdb():
    """
    # 将所有的没有记录到数据库中的重新进行记录
    # 当然本地有文件的可以尝试直接进行读取
    :return:
    """
    _have_formated_recodes = [x.scan_recode for x in ScanReport.objects.all() ]
    for x in ScanRecode.objects.all():
        if x not in _have_formated_recodes:
            ScanReport.objects.create(
                scan_recode=x,
                report=x.get_report_txt()
            )

### 访问日志基础统计接口
@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated, ))
def download_single_reporttxt(request):
    _data = request.data if request.method == "POST" else request.GET
    _scan_recode_id = str(_data["sid"])
    x = ScanRecode.objects.get(id=_scan_recode_id)
    res = x.get_report_txt()

    return HttpResponse(res)

import os, tempfile, zipfile
from datetime import datetime, date
from wsgiref.util import FileWrapper


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def download_zip(request):
    _data = request.data if request.method == "POST" else request.GET
    service_id = _data["sid"]

    # ScanCfg 里面的 Recode 记录的
    # OutputDir = os.path.join(RESULT_PATH, _temp["username"], _temp["workspace"], _temp["target"] ,_date)
    from scan.models import Service
    serv = Service.objects.get(id=str(service_id))

    workspace = serv.host.workspace.name
    usename = serv.host.workspace.user.username
    _date = str(serv.descover_time.date()).replace("-", "")
    target = str(serv.host.ip)

    from scan.models.scan_cfg import RESULT_PATH

    source_dir = os.path.join(RESULT_PATH, str(usename), str(workspace), target)
    temp = tempfile.TemporaryFile()
    zipf = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            ## 舍弃相对路径; 全部存储到一个文件
            ## arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            import re
            matched = re.match(".*?\-(\d+\.\d+\.\d+\.\d+)\-(\d+)\..*", filename)
            if matched:
                _port = matched.group(2)
                _target = matched.group(1)
                if _target == target and _port == serv.port :
                    zipf.write(pathfile, filename)

    zipf.close()

    response = StreamingHttpResponse(FileWrapper(temp), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename='+ workspace + '_' + target +'.zip'
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    # return response
    return response

