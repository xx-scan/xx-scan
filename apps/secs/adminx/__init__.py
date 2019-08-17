import xadmin


from  xadmin.filters import MultiSelectFieldListFilter
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from xadmin.plugins.inline import Inline
from secs.api.oauth.models import Community, Group


class GroupInline(object):
    model = Group
    # extra = 1
    # style = "accordion"


class CommunityAdmin(object):
    hidden_menu = True

    list_display = ("community_name", "group", "responsibility", "date_created")

    form_layout = (
        Main(
            Tab(
                "用户组",
                Inline(GroupInline),
                Fieldset(
                    "用户权限组", "group", description="针对操作管线的用户管理组进行责任划分。",
                ),
            ),
        ),
        Side(
            Tab(
                "责任",
                Fieldset(
                    "责任管理", "community_name", "responsibility", description="针对系统部件创建策略, 设置生效与否",
                ),
            ),

        )
    )


xadmin.site.register(Community, CommunityAdmin)