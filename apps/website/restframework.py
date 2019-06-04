REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES = 60

REST_FRAMEWORK_APPS = (
    'rest_framework',
    'rest_framework.authtoken',
)

APPEND_SLASH=False

# https://getblimp.github.io/django-rest-framework-jwt/
from services.api.oauth.local_jwt.jwt_settings import LocalJSONWebTokenAuthentication

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        #   设置访问权限为只读
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        #   设置访问权限为必须是用户
        'rest_framework.permissions.IsAuthenticated',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        LocalJSONWebTokenAuthentication,
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 增加 rest_framework_simplejwt ; 注释默认的 jwt
        #'rest_framework_simplejwt.authentication.JWTTokenUserAuthentication',
        ),

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10

}

from services.api.oauth.local_jwt.jwt_settings import JWT_AUTH
