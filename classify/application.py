# -*- coding:utf-8 -*-
"""
创建路由表
:Author:  WangYong
:Create:  2019/7/4 16:35
Copyright (c) 2019, Beike Group All Rights Reserved.
"""


import tornado.web
from classify import lushi_controller


class Application(tornado.web.Application):
    # 创建tornado.web.Application子类(继承),路由类
    def __init__(self):
        handler = [
            # 中转站接口
            (r'/lushi', lushi_controller.MyHandler)
        ]
        # 将参数传入父类
        super(Application, self).__init__(handler)