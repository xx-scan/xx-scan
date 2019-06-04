from django.conf.urls import url, include

from .views import scan_v1_router

urlpatterns_scan_v1 = [
    url(r'^scan/', include(scan_v1_router.urls)),
]
