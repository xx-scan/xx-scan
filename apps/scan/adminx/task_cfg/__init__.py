import xadmin
from xadmin.layout import Fieldset

from ...models import Scheme, ScanTask, Workspace
from website.settings import PREVILEGED_USER_SETS


from xadmin.plugins.inline import Inline, filter_hook
import xadmin
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side

class SchemeAdmin(object):
    list_display = ("name", "desc", "create_user", "date_created")
    # list_display = ("name", "desc", "scan_tools")
    # 用户只可以获取到自己的设置的方案了

    def queryset(self):
        qs = super(SchemeAdmin, self).queryset()
        if self.request.user.username in PREVILEGED_USER_SETS:
            return qs
        else:
            return qs.filter(create_user=self.request.user)

    def save_models(self):
        instance = self.new_obj
        request = self.request

        instance.create_user = request.user
        instance.save()

xadmin.sites.site.register(Scheme, SchemeAdmin)


class WorkspaceInline(object):
    model = Workspace
    extra = 1
    style = "accordion"

class ScanTaskInline(object):
    model = ScanTask
    extra = 1
    style = "accordion"


class ScanTaskAdmin(object):
    def queryset(self):
        qs = super(ScanTaskAdmin, self).queryset()
        if self.request.user.username in PREVILEGED_USER_SETS:
            return qs
        else:
            return qs.filter(workspace__user=self.request.user)



    list_display = ('targets', "ports", "imports_active", "scan_scheme", "date_created", )
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

    # wizard_form_list = fieldsets

    # inlines = [WorkspaceInline, ]

    form_layout = (
        Main(
            TabHolder(
                Tab(
                    "文件添加扫描",
                    Fieldset(
                        "基础扫描设置",
                        "workspace",
                        "scan_scheme",
                        Row("imports_active", "imports"),
                        Row("atnow", "regular"),
                    ),
                ),


            ),
        ),
        Side(
            Fieldset("自定义目标", 'targets', "ports", "udp", "domains"),
        )
    )

xadmin.site.register(ScanTask, ScanTaskAdmin)


class WorkspaceAdmin(object):

    def queryset(self):
        qs = super(WorkspaceAdmin, self).queryset()
        if self.request.user.username in PREVILEGED_USER_SETS:
            return qs
        else:
            return qs.filter(user=self.request.user)

    # readonly_fields = ('user', )
    def uniq_name(self, instance):
        return instance.name + "_" + instance.user.username

    uniq_name.short_description = "唯一ID"
    uniq_name.allow_tags = True
    uniq_name.is_column = True

    list_editable = ['name', 'summary']
    list_display = ('name', "user", 'uniq_name', 'summary', 'date_updated', )

    fieldsets = [("工作组名称", {'fields': ['name']}),
                 ('用户', {'fields': ['user'], 'classes': ['collapse']}), ]

    # form_layout = (
    #     Fieldset("名称", 'name', 'summary'),
    #     Fieldset(None, 'user', 'desc', 'id', **{"style": "display:None"}),
    # )

    inlines = [ScanTaskInline, ]

    actions = None
    # aggregate_fields = {"user_count": "sum", "view_count": "sum"}
    # refresh_times = (3, 5, 10)

    form_layout = (
        Main(
            TabHolder(
                Tab(
                    "创建扫描任务",
                    'name',
                    Inline(ScanTask),
                ),

            ),
        ),
        Side(
            Fieldset("名称", 'summary'),
            Fieldset(None, 'user', 'desc', 'id', **{"style": "display:None"}),
        )
    )

    def save_models(self):
        instance = self.new_obj
        request = self.request

        instance.user = request.user
        instance.save()

xadmin.site.register(Workspace, WorkspaceAdmin)