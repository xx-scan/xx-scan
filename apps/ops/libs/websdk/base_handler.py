#!/usr/bin/env python
# -*-coding:utf-8-*-

import shortuuid
from .cache import get_cache
from tornado.web import RequestHandler, HTTPError
from .jwt_token import AuthToken
from .jwt.api_settings import Authentication_KEY


class DevBaseHandler(RequestHandler):

    def __init__(self, *args, **kwargs):
        self.new_csrf_key = str(shortuuid.uuid())
        self.user = None
        super(DevBaseHandler, self).__init__(*args, **kwargs)

    def prepare(self):

        # 验证客户端CSRF，如请求为GET，则不验证，否则验证。最后将写入新的key
        cache = get_cache()
        if self.request.method not in ("GET", "HEAD", "OPTIONS"):
            csrf_key = self.get_cookie('csrf_key')
            pipeline = cache.get_pipeline()
            result = cache.get(csrf_key, private=False, pipeline=pipeline)
            cache.delete(csrf_key, private=False, pipeline=pipeline)
            if result != '1':
                raise HTTPError(402, 'CSRF-ERROR')

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

    def get(self, *args, **kwargs):
        self.write("Everything is OK!")


# 生产环境中使用的Handle开了Debug
class ProductRequestHandle(DevBaseHandler):

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.set_status(status_code)
            return self.finish('找不到相关路径-404')

        elif status_code == 400:
            self.set_status(status_code)
            return self.finish('错误请求')

        elif status_code == 402:
            self.set_status(status_code)
            return self.finish('CSRF错误')

        elif status_code == 403:
            self.set_status(status_code)
            return self.finish('访问阻断')

        elif status_code == 500:
            self.set_status(status_code)
            return self.finish('服务器内部错误')

        elif status_code == 401:
            self.set_status(status_code)
            return self.finish('登录验证失败')

        else:
            self.set_status(status_code)


from .configs import configs
BaseHandler = DevBaseHandler if configs.debug else ProductRequestHandle


class LivenessProbe(RequestHandler):

    def head(self, *args, **kwargs):
        self.write("I'm OK")

    def get(self, *args, **kwargs):
        self.write("I'm OK")
