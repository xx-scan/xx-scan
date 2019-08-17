#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author  : actanble
Date    : 2019/3/20
Desc    :
"""
from ops.libs.base_handler import BaseHandler
# from tornado.web import RequestHandler, HTTPError
from ops.libs.opssdk.operate.mail import Mail


class SendMailHandler(BaseHandler):
    def post(self, *args, **kwargs):
        Mail(mail_user="actanble", mail_pass="string123",).send_mail(to_list='2970090120@qq.com,180573956@qq.com,admin@actanble.com',
                                                                        header='无尘', sub='test000011',
                                                                        content="<div>?????</div>")
        self.write(dict(code=0, msg='send OK'))


mail_urls = [
    (r"/send_mail", SendMailHandler),
]


if __name__ == "__main__":
    pass
