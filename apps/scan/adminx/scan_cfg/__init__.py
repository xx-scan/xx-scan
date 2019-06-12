import xadmin


from ...models import ScanScript, ScanRecode, ScanTool, Scheme

class ScanScriptAdmin(object):
    hidden_menu = True

    list_display = ('name', "bin_name", "args", 'protocol', 'used_script')

xadmin.site.register(ScanScript, ScanScriptAdmin)


class ScanToolAdmin(object):
    list_display = ("name", "in_system", "protocol", "summary")

    fieldsets = [
        ("介绍", {'fields': ['name', "desc", "summary","help_scripts"]}),
        ('安装', {'fields': ['in_system', 'install']}),
        ('检查', {'fields': ['judge_script'], 'classes': ['collapse']}),
    ]

xadmin.site.register(ScanTool, ScanToolAdmin)


## 扫描 Recode 记录管理
class ScanRecodeAdmin(object):
    hidden_menu = True

    def queryset(self):
        from website.settings import PREVILEGED_USER_SETS
        qs = super(ScanRecodeAdmin, self).queryset()
        if self.request.user.username in PREVILEGED_USER_SETS:
            return qs
        else:
            return qs.filter(service__host__workspace__user=self.request.user)

    def show_report_txt(self, instance):
        return "<a href='{}'>文本查看</a>".format("/xx/scan/download_single_reporttxt?sid=" + str(instance.id))

    show_report_txt.short_description = "报告文本打开"
    show_report_txt.allow_tags = True
    show_report_txt.is_column = True

    list_display = ("service", "scan_tool", "active", "domain", "show_report_txt")

    #readonly_fields = ('create_user', )


xadmin.site.register(ScanRecode, ScanRecodeAdmin)


from ...models import ScanCfgUploads
class ScanCfgUploadsAdmin(object):
    list_display = ("name", "config_file", "desc", "date_created")

xadmin.site.register(ScanCfgUploads, ScanCfgUploadsAdmin)
