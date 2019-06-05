import xadmin


from ...models import ReportFormat, ScanReport

# class ScanReportAdmin(admin.ModelAdmin):
#     # ...
#     list_display = ('port', "port_name", "desc", 'type', 'type_desc', 'protocol')
#
#     fieldsets = [
#         ("端口", {'fields': ['port', "port_name", "desc"] }),
#         ('端口类型', {'fields': ['type' , 'type_desc']}),
#         ('归属协议', {'fields': ['protocol'], 'classes': ['collapse']}),
#     ]

# admin.site.register(ServicePort, ServicePortAdmin)



xadmin.site.register(ReportFormat)
xadmin.site.register(ScanReport)


