import xadmin
from xadmin.views import ModelAdminView

from scan.models import Host

class TestModelAdminView(ModelAdminView):

    def get(self, request, obj_id):
        return Host.objects.get(obj_id)


# xadmin.site.register_modelview(r'^(.+)/test/$', TestModelAdminView, name='%s_%s_test')


class ServiceRecordAdmin(object):



    data_charts = {
        "services_count": {'title': u"探测到的主机服务数量",
                       "x-field": "host",
                       "y-field": ("user_count", "view_count"),
                       "order": ('date',)},
        "avg_count": {'title': u"Avg Report",
                      "x-field": "date",
                      "y-field": ('avg_count',),
                      "order": ('date',)}
    }