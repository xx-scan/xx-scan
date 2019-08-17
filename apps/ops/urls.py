from django.conf.urls import url, include

urlpatterns = [

]

from .apscheduler.orm.views import djapscheduler_router
from .mail.views import mail_router

urlpatterns += [
    url(r'mail/', include(mail_router.urls)),
    url(r'dj_aps/', include(djapscheduler_router.urls)),
]
