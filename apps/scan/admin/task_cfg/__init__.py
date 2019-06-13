from django.contrib import admin


from ...models import Scheme, ScanTask, Workspace

class ScanTaskAdmin(admin.ModelAdmin):

    def schedule(self, obj=None, is_header=False):
        return obj.run_schedule()

    list_display = ('targets', "ports", "scan_scheme", "date_created", )
    # list_display = ('targets', "ports", "scan_scheme", "date_created", schedule)

    fieldsets = [
        # ("基本描述", {'fields': ['type', "name", "desc"] }),
        ('工作组', {'fields': ['workspace']}),
        ('文件导入', {'fields': ['imports_active' , 'imports']}),
        ('自定义目标', {'fields': ['targets', "ports", "udp", "domains"]}),
        ('选定扫描方案', {'fields': ['scan_scheme']}),
        ('执行类型', {'fields': ['atnow', "regular", "interval", "crontab"]}),
    ]

admin.site.register(ScanTask, ScanTaskAdmin)


class WorkspaceAdmin(admin.ModelAdmin):
    fieldsets = [("工作组名称", {'fields': ['name']}),
                 ('用户', {'fields': ['user'], 'classes': ['collapse']}), ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Workspace, WorkspaceAdmin)