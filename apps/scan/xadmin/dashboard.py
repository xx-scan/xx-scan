from __future__ import absolute_import

from collections import OrderedDict
from django.apps import apps
from xadmin.util import smart_text, capfirst, sortkeypicker
from xadmin.plugins.inline import Inline, filter_hook
import xadmin
from xadmin import views
# from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
# from xadmin.plugins.batch import BatchChangeAction


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
    site_footer = 'COPYRIGHT © 2010 - 2018 ALL RIGHTS RESERVED"'  # 底部版权
    # menu_style = 'accordion'  # 设置数据管理导航折叠，以每一个app为一个折叠框

    global_search_models = [Host, Workspace, Service, ScanRecode, ScanTool]
    global_models_icon = {
        Host: "fa fa-laptop", Workspace: "fa fa-cloud"
    }
    menu_style = 'accordion'  # 'accordion'  default

    apps_icons = {"home": "fa fa-home", "products": "", "companyintroduction": "",
                  "certifications": "fa fa-certificate",
                  "contactus": "fa fa-phone", "forum": "", "logisticinformation": "",
                  "sourcedownload": "fa fa-download", "trade": "fa fa-shopping-cart", "users": "fa fa-user",
                  "wechatuser": "fa fa-user", "knowledgebase": "fa fa-book", "questionanswer": "fa fa-question-circle"}


    @filter_hook
    def get_nav_menu(self):
        site_menu = list(self.get_site_menu() or [])
        had_urls = []

        def get_url(menu, had_urls):
            if 'url' in menu:
                had_urls.append(menu['url'])
            if 'menus' in menu:
                for m in menu['menus']:
                    get_url(m, had_urls)

        get_url({'menus': site_menu}, had_urls)

        nav_menu = OrderedDict()

        menus_ = self.admin_site._registry.items()
        for model, model_admin in menus_:
            if getattr(model_admin, 'hidden_menu', False):
                continue
            app_label = model._meta.app_label
            app_icon = None
            model_dict = {
                'title': smart_text(capfirst(model._meta.verbose_name_plural)),
                'url': self.get_model_url(model, "changelist"),
                'icon': self.get_model_icon(model),
                'perm': self.get_model_perm(model, 'view'),
                'order': model_admin.order,
            }
            if model_dict['url'] in had_urls:
                continue

            app_key = "app:%s" % app_label
            if app_key in nav_menu:
                nav_menu[app_key]['menus'].append(model_dict)
            else:
                # Find app title
                app_title = smart_text(app_label.title())
                if app_label.lower() in self.apps_label_title:
                    app_title = self.apps_label_title[app_label.lower()]
                else:
                    appL = apps.get_app_config(app_label)
                    app_title = smart_text(apps.get_app_config(app_label).verbose_name)
                    # added by Fiona for menu ordering
                    if app_label == "auth":
                        app_index = len(menus_) - 1
                    elif app_label == "xadmin":
                        app_index = len(menus_) - 2
                    else:
                        # app_index = appL.orderIndex_
                        app_index = 10
                # find app icon
                if app_label.lower() in self.apps_icons:
                    app_icon = self.apps_icons[app_label.lower()]
                nav_menu[app_key] = {
                    "orderIndex": app_index,
                    'title': app_title,
                    'menus': [model_dict],
                }
            app_menu = nav_menu[app_key]
            if app_icon:
                app_menu['first_icon'] = app_icon
            elif ('first_icon' not in app_menu or
                  app_menu['first_icon'] == self.default_model_icon) and model_dict.get('icon'):
                app_menu['first_icon'] = model_dict['icon']

            if 'first_url' not in app_menu and model_dict.get('url'):
                app_menu['first_url'] = model_dict['url']

        for menu in nav_menu.values():
            menu['menus'].sort(key=sortkeypicker(['order', 'title']))

        nav_menu = list(nav_menu.values())
        # nav_menu.sort(key=lambda x: x['title'])
        # 左侧菜单自定义排序新增
        nav_menu.sort(key=sortkeypicker(['orderIndex']))
        site_menu.extend(nav_menu)

        return site_menu


@xadmin.sites.register(views.BaseAdminView)
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True