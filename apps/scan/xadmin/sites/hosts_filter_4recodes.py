import xadmin
from xadmin.views import ModelAdminView
from xadmin.views import BaseAdminView
from django.http import HttpResponse
from django.shortcuts import render


from scan.models import Host


class TestModelAdminView(BaseAdminView):

    def get(self, request):

        return HttpResponse("TEST_VIEW")


xadmin.site.register_view(r'^test_view/$', TestModelAdminView, name='for_test')
# xadmin.site.register_modelview(r'^(.+)/test/$', TestModelAdminView, name='%s_%s_test')

class TestAdminView(BaseAdminView):

    def get(self, request):

        return render(request, "scan/base_add.html", {"datas": [i for i in range(100)]})

xadmin.site.register_view(r'^test/$', TestAdminView, name='test001')