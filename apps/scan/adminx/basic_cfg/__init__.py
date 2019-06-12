import xadmin

from ...models import PortRange, ServicePort, Protocol, NmapServiceName


class ServicePortAdmin(object):
    hidden_menu = True

    # ...
    list_display = ('port', "port_name", "desc", 'type', 'type_desc', 'protocol')

    fieldsets = [
        ("端口", {'fields': ['port', "port_name", "desc"] }),
        ('端口类型', {'fields': ['type' , 'type_desc']}),
        ('归属协议', {'fields': ['protocol'], 'classes': ['collapse']}),
    ]

xadmin.site.register(ServicePort, ServicePortAdmin)

class PortRangeAdmin(object):
    hidden_menu = True
    list_display = ("name", "ports")
xadmin.site.register(PortRange, PortRangeAdmin)

class NmapServiceAdmin(object):
    list_display = ('protocol', 'service_name')
xadmin.site.register(NmapServiceName, NmapServiceAdmin)

xadmin.site.register(Protocol)




