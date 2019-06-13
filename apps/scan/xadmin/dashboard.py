from __future__ import absolute_import

import xadmin
from xadmin import views


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


@xadmin.sites.register(views.BaseAdminView)
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


from .sites.nav_list import GlobalSetting