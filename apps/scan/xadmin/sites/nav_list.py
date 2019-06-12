from __future__ import absolute_import

from collections import OrderedDict
from django.apps import apps
from xadmin.util import smart_text, capfirst, sortkeypicker
from xadmin.plugins.inline import Inline, filter_hook
import xadmin
from xadmin import views
# from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
# from xadmin.plugins.batch import BatchChangeAction
from django.contrib.auth.models import Group, User, Permission

from scan.models import Host, ScanRecode, ScanScript, Service, Scheme, ScanTask, \
    ScanTool, ScanReport, ServicePort, ScanCfgUploads, NmapServiceName, \
    Workspace,ReportFormat, Protocol, PortRange

from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule


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

    def get_site_menu(self):
        return (
            {'title': '扫描任务设置', 'menus': (
                {'title': '开启扫描任务', 'url': self.get_model_url(ScanTask, 'changelist'), "icon":"fa fa-home"},
                {'title': '用户工作台', 'url': self.get_model_url(Workspace, 'changelist')},
                {'title': '扫描方案', 'url': self.get_model_url(Scheme, 'changelist')},
            ), "icon":"fa fa-phone"},
            {'title': '扫描结果查看', 'menus': (
                {'title': '探测主机', 'url': self.get_model_url(Host, 'changelist')},
                {'title': '探测服务', 'url': self.get_model_url(Service, 'changelist')},
                {'title': '二次探测记录', 'url': self.get_model_url(ScanRecode, 'changelist')},
            )},
            {'title': '扫描方案设置', 'menus': (
                {'title': '扫描方案上传', 'url': self.get_model_url(ScanCfgUploads, 'changelist')},
                {'title': '扫描脚本', 'url': self.get_model_url(ScanScript, 'changelist')},
                {'title': '待添加扫描工具', 'url': self.get_model_url(ScanTool, 'changelist')},
            ), "icon":"fa fa-certificate"},
            # {'title': '扫描报告处理', 'menus': (
            #     {'title': '扫描报告', 'url': self.get_model_url(ScanReport, 'changelist')},
            #     {'title': '报告格式化', 'url': self.get_model_url(ReportFormat, 'changelist')},
            # )},
            {'title': '其他工具', 'menus': (
                {'title': '扫描协议', 'url': self.get_model_url(Protocol, 'changelist')},
                {'title': '端口范围', 'url': self.get_model_url(PortRange, 'changelist')},
                {'title': '常见端口', 'url': self.get_model_url(ServicePort, 'changelist')},
                {'title': 'Nmap探测服务名', 'url': self.get_model_url(NmapServiceName, 'changelist')},
            ), "icon":"fa fa-book"},
            {'title': '定时器任务', 'menus': (
                {'title': '分段任务', 'url': self.get_model_url(PeriodicTask, 'changelist')},
                {'title': '间隔执行任务', 'url': self.get_model_url(IntervalSchedule, 'changelist')},
                {'title': 'Crontab执行任务', 'url': self.get_model_url(CrontabSchedule, 'changelist')},
            ), "icon":"fa fa-book"},

            {'title': '安全机制', 'menus': (
                {'title': '用户信息', 'url': self.get_model_url(User, 'changelist')},
                {'title': '组', 'url': self.get_model_url(Group, 'changelist')},
                {'title': '权限', 'url': self.get_model_url(Permission, 'changelist')},
            ), "icon":"fa fa-user"}
        )

