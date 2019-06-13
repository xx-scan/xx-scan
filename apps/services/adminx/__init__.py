from ..models import PlatOptHistory, UserAuditLog

import xadmin
from xadmin.layout import Fieldset


class PHLAdmin(object):
    list_display = ("desc", "extra", "type", 'opreate_time')

xadmin.site.register(PlatOptHistory, PHLAdmin)