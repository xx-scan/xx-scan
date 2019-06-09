from __future__ import absolute_import
import xadmin
from xadmin import views
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction

from scan.models import ScanTask, ScanRecode, Workspace, ScanTool, Host, Service


@xadmin.sites.register(views.website.IndexView)
class MainDashboard(object):
    widgets = [
        [
            {"type": "html", "title": "首页设置窗体",
             "content": "<h3> Welcome to XX-SCAN ! "
                        "</h3><p>XX-Scan : <br/>https://github.com/xx-scan/xx-scan/</p>"},
            {"type": "list", "model": "scan.host", "params": {"o": "-date_updated"}},
        ],
        [
            {"type": "qbutton", "title": "Quick Start",
             "btns": [{"model": Workspace},
                      {"model": ScanTool},
                      {"title": "Github", "url": "http://github.com/xx-scan/"}]},
            {"type": "addform", "model": Workspace},
        ]
    ]


# {"type": "chart", "model": "scan.workspace", "chart": "hosts_count",
#  "params": {"_p_ws_count_date__gte": "2013-01-08", "p": 1, "_p_ws_count_date__lt": "2019-06-29"}},


@xadmin.sites.register(views.CommAdminView)
class GlobalSetting(object):
    site_title = 'XXScan管控平台'  # 头部系统名称
    site_footer = 'XXScan管控平台，由actanble开发'  # 底部版权
    # menu_style = 'accordion'  # 设置数据管理导航折叠，以每一个app为一个折叠框

    global_search_models = [Host, Workspace, Service, ScanRecode, ScanTool]
    global_models_icon = {
        Host: "fa fa-laptop", Workspace: "fa fa-cloud"
    }
    menu_style = 'accordion'  # 'accordion'  default
