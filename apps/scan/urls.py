from django.conf.urls import url, include
#
# from .views import *

urlpatterns = [

]

from .api.orms.urls import scan_v1_router
urlpatterns += [url(r"^v1/", include(scan_v1_router.urls))]
