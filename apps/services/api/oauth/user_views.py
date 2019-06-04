# coding:utf-8
from datetime import datetime
from django.contrib.auth.models import User

from rest_framework import serializers, viewsets, routers
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


from .models import IdentityChoices, UserProfile

class CreateUserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(label=u'登录状态token', read_only=True)  # 增加token字段
    identity = serializers.ChoiceField(label=u'身份', choices=IdentityChoices, default='Guest')
    truename = serializers.CharField(label=u'真实姓名', max_length=20, default='')
    last_login = serializers.CharField(label=u'上次登陆', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'token', 'truename', 'identity', 'last_login')  # 增加token
        ## 'last_login', 'email', 'date_joined','is_staff', 'is_superuser',

    def create(self, validated_data):
        # user = super().create(**validated_data)
        user = User(username=validated_data["username"], password=validated_data["password"])
        # 调用django的认证系统加密密码
        user.set_password(validated_data['password'])
        user.last_login = datetime.now()
        user.email = validated_data["email"] if "email" in validated_data.keys() else "test@163.com"
        user.save()
        # 补充生成记录登录状态的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token

        # 增加用户的身份
        if validated_data["identity"] or validated_data["identity"] != '':
            identity = validated_data["identity"]
            passwd = validated_data['password']
            truename = validated_data['truename']

            UserProfile.objects.get_or_create(identity=identity,
                user=user, passwd=passwd, truename=truename)
            #user.truename = truename
            #user.identity = identity
        return user

    # def delete(self, pk):
    #     obj = self.get_object(pk)
    #     ## 2019-3-28 如果不是超级管理员不能执行操作
    #     if True:
    #         print(self.context)
    #         #return Response(status=402, data={"reason": "Can't Get Delete The Permision."})
    #     ## 2019-3-29 如果是本人不能执行删除自己的操作
    #
    #     return obj
    #     ## 对象同步删除
    #     conn_up = UserProfile.objects.filter(user=obj)
    #     conn_up.delete()
    #     try:
    #         obj.delete()
    #     except:
    #         pass
    #     return Response(status=status.HTTP_204_NO_CONTENT)



class JWTUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.IsAuthenticated, )


router = routers.DefaultRouter()
router.register(r'users', JWTUserViewSet)


## 2019-4-26 增加安全源内容审计的条目
from services.models import UserAuditLog
class UserAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuditLog
        #fields = ('url', 'request_method', 'ip', 'username', 'status', 'opreate_time', 'param')
        fields = ('ip', 'username', 'status', 'opreate_time')

class UserAuditLogViewSet(viewsets.ModelViewSet):
    queryset = UserAuditLog.objects.all()
    serializer_class = UserAuditLogSerializer
    permission_classes = (permissions.IsAuthenticated, )

router.register(r'plat_audit', UserAuditLogViewSet)
