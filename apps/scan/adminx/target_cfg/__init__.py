import xadmin


from ...models import Host, Service


class HostAdmin(object):
    list_display = ("name", "ip", "mac", "mac_vendor", "up")
    list_editable = ['name', 'extra', 'comment', 'domain']

xadmin.site.register(Host, HostAdmin)

class ServiceAdmin(object):
    search_fields = ("port", "host__ip", "service", "state", 'protocol')
    list_display = ("host", "port", "state", "banner", "protocol", "service", "version", "descover_time")

    list_export = ('xls', 'xml', 'json')
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