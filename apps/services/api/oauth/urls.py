# coding:utf-8
from django.conf.urls import url, include

# from rest_framework_jwt.views import obtain_jwt_token
# from rest_framework_jwt.views import refresh_jwt_token
# from rest_framework_jwt.views import verify_jwt_token
from services.api.oauth.local_jwt.jwt_views import obtain_jwt_token, verify_jwt_token

# from .views import *
from .user_views import router

urlpatterns = [
    url(r'^oauth/', include(router.urls) ),
]

# from .customizer_obtain import customize_obtain_jwt_token
urlpatterns2 = [
    # url('customize_login/', customize_obtain_jwt_token), ## 自定义登陆令牌调控

    url('jwt_login/$', obtain_jwt_token),     ## 生成令牌
    # url('refresh_jwt_token/$', refresh_jwt_token), ## 刷新令牌
    url('verify_jwt_token/$', verify_jwt_token),  ## 验证令牌
    url('rf_api/', include('rest_framework.urls', namespace='rest_framework')), ### 测试中用到; 生产环境删除
]

urlpatterns += urlpatterns2

### 测试部分
# from .jwt import urlpatterns as tparten
# urlpatterns.extend(tparten)

from .views import get_all_users, user_delete, logout
urlpatterns += [
    url('users/user_lists$', get_all_users),
    url('user/(?P<pk>[0-9]+)/$', user_delete),
    url('user/logout$', logout)
]

