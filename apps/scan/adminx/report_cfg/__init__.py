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
class ScanReportAdmin(object):
    def queryset(self):
        from website.settings import PREVILEGED_USER_SETS
        qs = super(ScanReportAdmin, self).queryset()
        if self.request.user.username in PREVILEGED_USER_SETS:
            return qs
        else:
            return qs.filter(scan_recode__service__host__workspace__user=self.request.user)

    list_display = ("scan_recode", "report", "date_created")


# xadmin.site.register(ReportFormat)
# xadmin.site.register(ScanReport, ScanReportAdmin)
#

## 2019-6-12 关闭报告初始化和内容