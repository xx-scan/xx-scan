# coding:utf-8
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from django.http import StreamingHttpResponse

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
def get_report_by_output_path(request):
    _data = request.data if request.method == "POST" else request.GET
    _scan_recode_id = _data["sid"]
    try:
        ScanRecode.objects.get()
        return StreamingHttpResponse()

    except:
        return Response({"stat":False, "reason": "Objects not Exist!"})





