# coding:utf-8
import json
from django.http import JsonResponse
from rest_framework.response import Response

# from django.forms.models import model_to_dict
from django.core.paginator import Paginator

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from secs.utils.db_utils import from_sql_get_data
# from .local_config import AccessLogPaginator, ModsecLogPaginator


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_all_users(request):
    # data = json.loads(request.body.decode())
    data = request.GET
    pager = data["page"] if "page" in data.keys() else 1
    query_sql = """select auth_user.id as uid, username, date_joined, email, identity, last_login, truename from auth_user 
      left join userprofile on auth_user.id = userprofile.user_id order by date_joined desc;"""
    p = Paginator(from_sql_get_data(query_sql)["data"], 10)

    all_counts = p.count  # 对象总数
    page_count = p.num_pages  # 总页数
    pj = p.page(pager)
    objs = pj.object_list
    res_data = objs ## 主要的对象
    return Response({"res": res_data, "page_count": page_count, "pager": pager, "all_counts": all_counts})


@api_view(['DELETE'])
@permission_classes((IsAuthenticated, ))
def user_delete(request, pk):
    # data = json.loads(request.body.decode())
    _obj = from_sql_get_data("""select * from auth_user where id='{}';""".format(str(pk)))["data"]
    if len(_obj) < 1:
        return Response(status=204, data={"result": "Not Found This Object."})
    uname = _obj[0]["username"]

    _user = request.user ##
    _visitor = _user.username
    if uname == _visitor:
        return Response(status=204, data={"result": "You Can't Opreate Yourself."})

    ### 2019-3-28 不能自己删除自己
    _userprofile = from_sql_get_data("""select * from (select auth_user.id as uid, username, date_joined, email, identity, last_login, truename from auth_user 
      left join userprofile on auth_user.id = userprofile.user_id) as main_user where username='{}';""".format(_visitor) )["data"]

    if len(_userprofile) < 1:
        return Response(status=204, data={"result": "You have not Authed."})

    ### 必须管理员才能删除
    if _userprofile[0]["identity"] != "SuperManager":
        return Response(status=204, data={"result": "Not Permit to Opreate."})

    flag = False
    try:
        from secs.models import UserProfile
        UserProfile.objects.filter(username=uname).delete()
    except:
        pass
    finally:
        from django.contrib.auth.models import User
        try:
            User.objects.get(id=int(pk)).delete()
            flag = True
        except:
            flag = False
    return Response(status=201, data={"result": "Delete Success.", "flag": flag})

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def logout(request):
    """
    登出用户的接口
    :param request:
    :return:
    """
    # from secs.models import UserAuditLog


    return Response(status= 200, data={"stat": True, "desc":"Logout from Platform."})