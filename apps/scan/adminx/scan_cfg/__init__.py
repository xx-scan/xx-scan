import xadmin


from ...models import ScanScript, ScanRecode, ScanTool, Scheme

class ScanScriptAdmin(object):
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


class ScanRecodeAdmin(object):

    list_display = ("service", "scan_tool", "active", "domain")

xadmin.site.register(ScanRecode, ScanRecodeAdmin)


class SchemeAdmin(object):
    list_display = ("name", "desc",)
    # list_display = ("name", "desc", "scan_tools")

xadmin.site.register(Scheme, SchemeAdmin)
