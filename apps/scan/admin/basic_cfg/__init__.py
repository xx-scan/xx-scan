from django.contrib import admin


from ...models import PortRange, ServicePort, Protocol

class ServicePortAdmin(admin.ModelAdmin):
    # ...
    list_display = ('port', "port_name", "desc", 'type', 'type_desc', 'protocol')

    fieldsets = [
        ("端口", {'fields': ['port', "port_name", "desc"] }),
        ('端口类型', {'fields': ['type' , 'type_desc']}),
        ('归属协议', {'fields': ['protocol'], 'classes': ['collapse']}),
    ]

admin.site.register(ServicePort, ServicePortAdmin)


class PortRangeAdmin(admin.ModelAdmin):
    list_display = ("name", "ports")

admin.site.register(PortRange, PortRangeAdmin)

admin.site.register(Protocol)


