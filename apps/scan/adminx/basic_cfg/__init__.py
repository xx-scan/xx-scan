import xadmin

from ...models import PortRange, ServicePort, Protocol

class ServicePortAdmin(object):
    # ...
    list_display = ('port', "port_name", "desc", 'type', 'type_desc', 'protocol')

    fieldsets = [
        ("端口", {'fields': ['port', "port_name", "desc"] }),
        ('端口类型', {'fields': ['type' , 'type_desc']}),
        ('归属协议', {'fields': ['protocol'], 'classes': ['collapse']}),
    ]

xadmin.site.register(ServicePort, ServicePortAdmin)


class PortRangeAdmin(object):
    list_display = ("name", "ports")

xadmin.site.register(PortRange, PortRangeAdmin)
xadmin.site.register(Protocol)




