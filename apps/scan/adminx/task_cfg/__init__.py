import xadmin


from ...models import Scheme, ScanTask, Workspace

class ScanTaskAdmin(object):

    def schedule(self, obj=None, is_header=False):
        return obj.run_schedule()

    list_display = ('targets', "ports", "scan_scheme", "date_created", )
    # list_display = ('targets', "ports", "scan_scheme", "date_created", schedule)
    list_editable = ['imports_active', 'workspace']

    fieldsets = [
        # ("基本描述", {'fields': ['type', "name", "desc"] }),
        ('工作组', {'fields': ['workspace']}),
        ('文件导入', {'fields': ['imports_active' , 'imports']}),
        ('自定义目标', {'fields': ['targets', "ports", "udp", "domains"]}),
        ('选定扫描方案', {'fields': ['scan_scheme']}),
        ('执行类型', {'fields': ['atnow', "regular", "interval", "crontab"]}),
    ]

xadmin.site.register(ScanTask, ScanTaskAdmin)


@xadmin.site.register(Workspace)
class WorkspaceAdmin(object):

    def uniq_name(self, instance):
        return instance.name + "_" + instance.user.username

    def hosts_count(self, instance):
        from scan.models import Host
        return len(Host.objects.filter(workspace=instance))

    uniq_name.short_description = "唯一ID"
    uniq_name.allow_tags = True
    uniq_name.is_column = True

    hosts_count.short_description = "主机数统计"
    hosts_count.allow_tags = True
    hosts_count.is_column = True

    list_editable = ['name', 'summary']
    list_display = ('name', "user", 'summary', 'date_updated', 'hosts_count')
    fieldsets = [("工作组名称", {'fields': ['name']}),
                 ('用户', {'fields': ['user'], 'classes': ['collapse']}), ]

    actions = None
    # aggregate_fields = {"user_count": "sum", "view_count": "sum"}
    #
    # refresh_times = (3, 5, 10)
    data_charts = {
        "主机统计": {'title': u"用户空间主机统计", "x-field": "uniq_name", "y-field": ("hosts_count",),
                       "order": ('date_updated',)},
    }


    def save_model(self, request, obj, form, change):
        obj.user = request.user

        # 检查当前访问空间中有没有; 如果有返回403


        super().save_model(request, obj, form, change)

