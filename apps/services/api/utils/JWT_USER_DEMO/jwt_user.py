from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, routers

from rest_framework_jwt.settings import api_settings
class CreateUserSerializer(serializers.ModelSerializer):
    """
    创建用户序列化器; 可以跟 models 类似添加字段。
    """
    token = serializers.CharField(label='登录状态token', read_only=True)  # 增加token字段
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token')  # 增加token
        ## 'last_login', 'email', 'date_joined','is_staff', 'is_superuser',

    def create(self, validated_data):
        user = super().create(validated_data)
        # 调用django的认证系统加密密码
        user.set_password(validated_data['password'])
        user.save()
        # 补充生成记录登录状态的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        return user

## 基本上没有有 延续上面的这个函数，
def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': CreateUserSerializer(user, context={'request': request}).data
    }

# ViewSets define the view behavior.
class JWTUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', JWTUserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^webauth/', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

urlpatterns2 = [
    url('jwt_login/$', obtain_jwt_token),     ## 生成令牌
    url('refresh_jwt_token/$', refresh_jwt_token), ## 刷新令牌
    url('verify_jwt_token/$', verify_jwt_token),  ## 验证令牌
    url('rf_api/', include('rest_framework.urls', namespace='rest_framework')), ### 测试中用到; 生产环境删除
]

urlpatterns.extend(urlpatterns2)

### 测试部分
# from .jwt import urlpatterns as tparten
# urlpatterns.extend(tparten)



