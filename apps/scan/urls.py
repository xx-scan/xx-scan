from django.conf.urls import url, include
#
# from .views import *

urlpatterns = [

]

from .api.orms.urls import scan_v1_router
urlpatterns += [url(r"^v1/", include(scan_v1_router.urls))]


from scan.api.mudules.scan_v2.report import download_single_reporttxt, download_zip
urlpatterns += [
    url(r"^download_single_reporttxt", download_single_reporttxt),
    url(r"^download_zip_by_service", download_zip)

]