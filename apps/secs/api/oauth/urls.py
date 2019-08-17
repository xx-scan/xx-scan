# coding:utf-8
from django.conf.urls import url, include

# from rest_framework_jwt.views import obtain_jwt_token
# from rest_framework_jwt.views import refresh_jwt_token
# from rest_framework_jwt.views import verify_jwt_token
from ..oauth.local_jwt.jwt_views import obtain_jwt_token, verify_jwt_token
from .vue_view import user_info, user_logout

# from .customizer_obtain import customize_obtain_jwt_token
urlpatterns = [
    # url('customize_login/', customize_obtain_jwt_token), ## 自定义登陆令牌调控
    url('^user/login$', obtain_jwt_token),
    url('^user/info$', user_info),
    url('^user/logout$', user_logout),
    # url('refresh_jwt_token/$', refresh_jwt_token),
    url('^verify_jwt_token/$', verify_jwt_token),
    url('^rf_api/', include('rest_framework.urls', namespace='rest_framework')),
]
