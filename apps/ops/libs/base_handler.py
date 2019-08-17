# !/usr/bin/env python
# -*-coding:utf-8-*-

import shortuuid
from ops.libs.websdk.base_handler import get_cache, BaseHandler as SDKBaseHandler
from tornado.web import RequestHandler, HTTPError
# import jwt
from ops.libs.websdk.jwt_token import AuthToken
from ops.libs.websdk.jwt.api_settings import Authentication_KEY


class BaseHandler(SDKBaseHandler):

    def __init__(self, *args, **kwargs):
        self.new_csrf_key = str(shortuuid.uuid())
        self.user = None
        super(BaseHandler, self).__init__(*args, **kwargs)

    def prepare(self):

        # 验证客户端CSRF，如请求为GET，则不验证，否则验证。最后将写入新的key
        cache = get_cache()
        if self.request.method not in ("GET", "HEAD", "OPTIONS"):
            csrf_key = self.get_cookie('csrf_key')
            pipeline = cache.get_pipeline()
            result = cache.get(csrf_key, private=False, pipeline=pipeline)
            cache.delete(csrf_key, private=False, pipeline=pipeline)
            if result != '1':
                raise HTTPError(402, 'csrf error')

        cache.set(self.new_csrf_key, 1, expire=1800, private=False)
        self.set_cookie('csrf_key', self.new_csrf_key)

        # 登陆验证
        auth_key = self.get_cookie('auth_key', None)
        if not auth_key:
            if Authentication_KEY in self.request.headers.keys():
                try:
                    auth_key = self.request.headers[Authentication_KEY].split()[1]
                except:
                    print("不是 JWT-token 格式")

        if not auth_key:
            url_auth_key = self.get_argument('auth_key', default=None, strip=True)
            if url_auth_key:
                auth_key = bytes(url_auth_key, encoding='utf-8')

        if not auth_key:
            raise HTTPError(401, '用户认证失败')

        user_info = AuthToken().decode_auth_token(auth_key)
        self.user = user_info


from website.settings import DEBUG
BaseHandler = BaseHandler if not DEBUG else RequestHandler