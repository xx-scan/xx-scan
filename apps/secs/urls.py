from django.conf.urls import url
#
# from .views import *

urlpatterns = [

]


#### jwt用户模块
from .api.oauth.urls import urlpatterns as user_upt
urlpatterns.extend(user_upt)
