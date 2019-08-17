#!/usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
from .jwt.utils import jwt_decode_handler, jwt_encode_handler


class AuthToken:

    def encode_auth_token(self, user):
        """
        django user 对象 或者包含Django user对象的一个列表
      :param user:
        :return:
        """
        try:
            return jwt_encode_handler(user)
        except Exception as e:
            return e

    def decode_auth_token(self, auth_token):
        """
         验证Token
        :param auth_token:
        :return: dict
        """
        return jwt_decode_handler(auth_token)


def gen_md5(pd):
    m2 = hashlib.md5()
    m2.update(pd.encode("utf-8"))
    return m2.hexdigest()
