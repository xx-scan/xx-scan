import xadmin
from xadmin.layout import Fieldset

from ...models import Scheme, ScanTask, Workspace
from website.settings import PREVILEGED_USER_SETS


class SchemeAdmin(object):
    list_display = ("name", "desc",)
    # list_display = ("name", "desc", "scan_tools")
    ## 职能获取到自己的设置的方案了

    def queryset(self):
        qs = super(SchemeAdmin, self).queryset()
        if self.request.user.username in PREVILEGED_USER_SETS:
            return qs
        else:
            return qs.filter(create_user=self.request.user)


xadmin.sites.site.register(Scheme, SchemeAdmin)

class ScanTaskAdmin(object):
    def queryset(self):
        qs = super(ScanTaskAdmin, self).queryset()
        if self.request.user.username in PREVILEGED_USER_SETS:
            return qs
        else:
            return qs.filter(workspace__user=self.request.user)

    def schedule(self, obj=None, is_header=False):
        return obj.run_schedule()

    list_display = ('targets', "ports", "scan_scheme", "date_created", )
    # list_display = ('targets', "ports", "scan_scheme", "date_created", schedule)
    list_editable = ['imports_active', 'workspace']

    # fieldsets = [
    #     # ("基本描述", {'fields': ['type', "name", "desc"] }),
    #     ('工作组', {'fields': ['workspace']}),
    #     ('文件导入', {'fields': ['imports_active' , 'imports']}),
    #     ('自定义目标', {'fields': ['targets', "ports", "udp", "domains"]}),
    #     ('选定扫描方案', {'fields': ['scan_scheme']}),
    #     ('执行类型', {'fields': ['atnow', "regular", "interval", "crontab"]}),
    # ]

    wizard_form_list = [
        ('工作组', {'fields': ['workspace']}),
        ('文件导入', {'fields': ['imports_active', 'imports']}),
        ('自定义目标', {'fields': ['targets', "ports", "udp", "domains"]}),
        ('选定扫描方案', {'fields': ['scan_scheme']}),
        ('执行类型', {'fields': ['atnow', "regular", "interval", "crontab"]}),
    ]


xadmin.site.register(ScanTask, ScanTaskAdmin)


class WorkspaceAdmin(object):

    def queryset(self):
        qs = super(WorkspaceAdmin, self).queryset()
        if self.request.user.username in PREVILEGED_USER_SETS:
            return qs
        else:
            return qs.filter(user=self.request.user)

    # readonly_fields = ('user', )



    def uniq_name(self, instance):
        return instance.name + "_" + instance.user.username

    uniq_name.short_description = "唯一ID"
    uniq_name.allow_tags = True
    uniq_name.is_column = True

    def hosts_count(self, instance):
        from scan.models import Host
        return len(Host.objects.filter(workspace=instance))
    hosts_count.short_description = "主机数统计"
    hosts_count.allow_tags = True
    hosts_count.is_column = True

    def services_count(self, instance):
        from scan.models import Service
        return len(Service.objects.filter(host__workspace=instance))
    services_count.short_description = "扫描出的服务数统计"
    services_count.allow_tags = True
    services_count.is_column = True


    def recodes_count(self, instance):
        from scan.models import ScanRecode
        return len(ScanRecode.objects.filter(service__host__workspace=instance))
    recodes_count.short_description = "服务执行脚本数统计"
    recodes_count.allow_tags = True
    recodes_count.is_column = True


    def ws_count_date(self, instance):
        return str(instance.date_updated.date())

    ws_count_date.short_description = "工作台日期"
    ws_count_date.allow_tags = True
    ws_count_date.is_column = True

    list_editable = ['name', 'summary']
    list_display = ('name', "user", 'uniq_name', 'summary', 'date_updated', 'hosts_count', 'recodes_count')

    fieldsets = [("工作组名称", {'fields': ['name']}),
                 ('用户', {'fields': ['user'], 'classes': ['collapse']}), ]

    form_layout = (
        Fieldset("名称", 'name', 'summary'),
        Fieldset(None, 'user', 'desc', 'id', **{"style": "display:None"}),
    )

    actions = None
    # aggregate_fields = {"user_count": "sum", "view_count": "sum"}
    # refresh_times = (3, 5, 10)
    data_charts = {
        "探测统计": {'title': u"扫描探测的主机统计", "x-field": "uniq_name",
                     "y-field": ("hosts_count", 'services_count', 'recodes_count'),
                     "option": {
                         "series": {"bars": {"align": "center", "barWidth": 0.3, 'show': True}},
                         "xaxis": { "mode": "categories"},
                     },
                    },

        "工作台创建统计": {'title': u"工作台创建统计", "x-field": "ws_count_date",
                 "y-field": ("ws_count_date", ),
                 "option": {
                     "series": {"bars": {"align": "center", "barWidth": 0.4, 'show': True}}, ## True是柱状图
                     "xaxis": {"aggregate": "count", "mode": "categories"},
                 },
                 },
        }

    def save_models(self):
        instance = self.new_obj
        request = self.request

        instance.user = request.user
        instance.save()

xadmin.site.register(Workspace, WorkspaceAdmin)