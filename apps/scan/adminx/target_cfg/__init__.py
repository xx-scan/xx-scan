import xadmin

from website.settings import PREVILEGED_USER_SETS
from ...models import Host, Service, ScanRecode


class HostAdmin(object):

    def queryset(self):
        qs = super(HostAdmin, self).queryset()

        if self.request.user.username in PREVILEGED_USER_SETS:
            return qs
        else:
            return qs.filter(workspace__user=self.request.user)

    def host_service_count(self, instance):
        return len(Service.objects.filter(host=instance))
    host_service_count.short_description = "主机服务数"
    host_service_count.allow_tags = True
    host_service_count.is_column = True

    def service_recode_count(self, instance):
        return len(ScanRecode.objects.filter(service__host=instance))
    service_recode_count.short_description = "二次扫描记录"
    service_recode_count.allow_tags = True
    service_recode_count.is_column = True

    def host_ip(self, instance):
        return instance.ip
    host_ip.short_description = "主机唯一键IP"
    host_ip.allow_tags = True
    host_ip.is_column = True

    list_display = ("name", "ip", "mac", "mac_vendor", "up", 'host_service_count')
    list_editable = ['name', 'extra', 'comment', 'domain']

    list_export = ('xls', 'xml', 'json')

    data_charts = {
        "主机服务统计": {'title': u"服务记录基本统计", "x-field": "host_ip",
                   "y-field": ('host_service_count', 'service_recode_count'),
                   "option": {
                       "series": {"bars": {"align": "center", "barWidth": 0.3, 'show': True}},
                       "xaxis": {"mode": "categories"},
                   },
        },
    }

xadmin.site.register(Host, HostAdmin)


class ServiceAdmin(object):

    def queryset(self):
        qs = super(ServiceAdmin, self).queryset()
        if self.request.user.username in PREVILEGED_USER_SETS:
            return qs
        else:
            return qs.filter(host__workspace__user=self.request.user)

    search_fields = ("port", "host__ip", "service", "state", 'protocol')
    list_display = ("host", "port", "state", "banner", "protocol", "service", "version", "descover_time")
    list_export = ('xls', 'xml', 'json')

    def service_recode_count(self, instance):
        return len(ScanRecode.objects.filter(service=instance))
    service_recode_count.short_description = "二次扫描记录"
    service_recode_count.allow_tags = True
    service_recode_count.is_column = True

    def uniq_id(self, instance):
        return instance.host.ip + "(" + str(instance.port) + ")[" + instance.service + "]"
    uniq_id.short_description = "服务"
    uniq_id.allow_tags = True
    uniq_id.is_column = True


    data_charts = {
        "主机服务统计": {'title': u"服务记录基本统计", "x-field": "uniq_id",
                 "y-field": ('service_recode_count'),
                 "option": {
                     "series": {"bars": {"align": "center", "barWidth": 0.3, 'show': True}},
                     "xaxis": {"mode": "categories"},
                 },
                 },
    }

    refresh_times = (5, 10, 20)

    ## 书签使用异常。
    list_bookmarks = [{
        'title': "TCP协议扫描出的服务",  # 书签的名称, 显示在书签菜单中
        'query': {'port': 80},  # 过滤参数, 是标准的 queryset 过滤
        'order': ('-descover_time',),  # 排序参数
        'cols': ( 'port', 'service', 'state', 'protocol', 'banner'),  # 显示的列
        #'search': 'tcp'  # 搜索参数, 指定搜索的内容
        },
        {
            'title': "开放状态的服务",  # 书签的名称, 显示在书签菜单中
            'query': {'state': "open"},  # 过滤参数, 是标准的 queryset 过滤
            'order': ('-descover_time', ),  # 排序参数
            'cols': ( 'port', 'service', 'state', 'protocol', 'banner'),  # 显示的列
            #'search': 'open'  # 搜索参数, 指定搜索的内容
        },
    ]



xadmin.site.register(Service, ServiceAdmin)