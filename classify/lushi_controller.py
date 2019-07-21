# -*- coding:utf-8 -*-
"""
定义对应的接口
:Author:  WangYong
:Create:  2019/7/4 17:34
Copyright (c) 2019, Beike Group All Rights Reserved.
"""

from classify import process_service
from tornado.web import RequestHandler


# 视图
class MyHandler(RequestHandler):

    # 中转处理接口
    def post(self, *args, **kwargs):
        request_body = self.request.body.decode("utf-8")
        proc = process_service.Process(request_body)
        self.write(proc.my_service())
