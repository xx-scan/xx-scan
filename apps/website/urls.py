from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [

      url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
      url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS

      url(r'^', admin.site.urls), # 2019-6-3 修改这个为首页

      url(r'^xx/mg/', include("services.urls")),
      url(r'^xx/scan/', include("scan.urls")),
      #url(r'^cso/v1/', include("scan.urls")), ## 管理

  ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
