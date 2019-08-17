from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib import admin

urlpatterns = [
      # url(r'^admin/', admin.site.urls),
      url(r'^cso/mg/', include("secs.urls")),
      url(r'^cso/v1/', include("mgsd.urls")),
      url(r'^cso/agent/', include("agent.urls")),
      url(r'^cso/ops/', include("ops.urls")),
  ]


urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)
urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
