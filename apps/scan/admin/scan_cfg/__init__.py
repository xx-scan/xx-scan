from django.contrib import admin


from ...models import ScanScript, ScanRecode, ScanTool, Scheme

class ScanScriptAdmin(admin.ModelAdmin):
    list_display = ('name', "bin_name", "args", 'protocol', 'used_script')

admin.site.register(ScanScript, ScanScriptAdmin)


class ScanToolAdmin(admin.ModelAdmin):
    list_display = ("name", "in_system", "protocol", "summary")

    fieldsets = [
        ("介绍", {'fields': ['name', "desc", "summary","help_scripts"]}),
        ('安装', {'fields': ['in_system', 'install']}),
        ('检查', {'fields': ['judge_script'], 'classes': ['collapse']}),
    ]

admin.site.register(ScanTool, ScanToolAdmin)


class ScanRecodeAdmin(admin.ModelAdmin):

    list_display = ("service", "scan_tool", "active", "domain")

admin.site.register(ScanRecode, ScanRecodeAdmin)


class SchemeAdmin(admin.ModelAdmin):
    list_display = ("name", "desc",)
    # list_display = ("name", "desc", "scan_tools")



admin.site.register(Scheme, SchemeAdmin)
