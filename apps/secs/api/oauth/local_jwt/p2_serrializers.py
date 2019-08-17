import jwt

from calendar import timegm
from datetime import datetime, timedelta

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework_jwt.compat import Serializer

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.compat import get_username_field, PasswordField


User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


# 增加登陆尝试的相关接口
# from ..login_fail_frequent_util import UserCache

from .p2_util import LoginOpreation

class JSONWebTokenSerializer(Serializer):
    """
    Serializer class used to validate a username and password.

    'username' is identified by the custom UserModel.USERNAME_FIELD.

    Returns a JSON Web Token that can be used to authenticate later calls.
    """
    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super(JSONWebTokenSerializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField(write_only=True)

    @property
    def username_field(self):
        return get_username_field()

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }
        _username = credentials[self.username_field]

        ######## 获取 IP ########
        _request = self.context["request"]
        if 'HTTP_X_FORWARDED_FOR' in _request.META.keys():
            ip = _request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = _request.META['REMOTE_ADDR']
        ######## 获取 IP 结束########

        ## 仍然在封禁时间段内的判断
        if not LoginOpreation(username=_username, ip=ip).check_stat():
            #msg = _('Accout is fips BlackList(Idb) and You Can Login After A While')
            msg = _('账户正处于封禁登陆的状态, 请过段时间再尝试登陆。')
            raise serializers.ValidationError(msg)

        if all(credentials.values()):
            user = authenticate(**credentials)
            # from secs.api.oauth.utils.local_authenticate import l_authenticate
            # user = l_authenticate(**credentials)
            if user:
                if not user.is_active:
                    # msg = _('User account is disabled.')
                    msg = _('账户不可用。')
                    raise serializers.ValidationError(msg)
                ### 登录成功
                # UserCache(username=_username).seccuss_cache_init() # 成功登陆后清理
                LoginOpreation(username=_username, ip=ip).login_sucess()
                # 单点登陆 START
                user.last_login = datetime.now()
                user.save()
                # 单点登陆 END
                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                ### 用户名和密码失败
                # _msg = UserCache(username=_username).failed_cache_init()["msg"]
                # msg = _('Unable to log fips with provided credentials.')
                LoginOpreation(username=_username, ip=ip).login_faild()
                # msg = _("PassWord And Username Not matched.")
                msg = _("用户名和密码不匹配。")
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)


class VerificationBaseSerializer(Serializer):
    """
    Abstract serializer used for verifying and refreshing JWTs.
    """
    token = serializers.CharField()

    def validate(self, attrs):
        msg = 'Please define a validate method.'
        raise NotImplementedError(msg)

    def _check_payload(self, token):
        # Check payload valid (based off of JSONWebTokenAuthentication,
        # may want to refactor)
        try:
            payload = jwt_decode_handler(token)
            # 单点登陆测试
            username = jwt_get_username_from_payload(payload)
            user = User.objects.get_by_natural_key(username)
            if "last_login" in payload.keys():
                if payload["last_login"] != str(user.last_login):
                    msg = _('Single Login Required.')
                    raise serializers.ValidationError(msg)
            # 单点登陆测试 END
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise serializers.ValidationError(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise serializers.ValidationError(msg)

        return payload

    def _check_user(self, payload):
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = _('Invalid payload.')
            raise serializers.ValidationError(msg)

        # Make sure user exists
        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            msg = _("User doesn't exist.")
            raise serializers.ValidationError(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise serializers.ValidationError(msg)

        return user


class VerifyJSONWebTokenSerializer(VerificationBaseSerializer):
    """
    Check the veracity of an access token.
    """

    def validate(self, attrs):
        token = attrs['token']

        payload = self._check_payload(token=token)
        user = self._check_user(payload=payload)

        return {
            'token': token,
            'user': user
        }


class RefreshJSONWebTokenSerializer(VerificationBaseSerializer):
    """
    Refresh an access token.
    """

    def validate(self, attrs):
        token = attrs['token']

        payload = self._check_payload(token=token)
        user = self._check_user(payload=payload)
        # Get and check 'orig_iat'
        orig_iat = payload.get('orig_iat')

        if orig_iat:
            # Verify expiration
            refresh_limit = api_settings.JWT_REFRESH_EXPIRATION_DELTA

            if isinstance(refresh_limit, timedelta):
                refresh_limit = (refresh_limit.days * 24 * 3600 +
                                 refresh_limit.seconds)

            expiration_timestamp = orig_iat + int(refresh_limit)
            now_timestamp = timegm(datetime.utcnow().utctimetuple())

            if now_timestamp > expiration_timestamp:
                msg = _('Refresh has expired.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('orig_iat field is required.')
            raise serializers.ValidationError(msg)

        new_payload = jwt_payload_handler(user)
        new_payload['orig_iat'] = orig_iat

        return {
            'token': jwt_encode_handler(new_payload),
            'user': user
        }
