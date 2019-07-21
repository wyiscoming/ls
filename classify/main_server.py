# -*- coding:utf-8 -*-
"""
启动服务器
:Author:  WangYong
:Create:  2019/7/4 16:14
Copyright (c) 2019, Beike Group All Rights Reserved.
"""
from classify.conf import base_conf
import tornado.httpserver
import tornado.ioloop
import tornado.web
from classify.application import Application


if __name__ == '__main__':
    # 路由
    app = Application()
    # 服务
    http_server = tornado.httpserver.HTTPServer(app)
    # 端口号
    http_server.listen(base_conf.OPTIONS['port'])
    # 启动服务
    http_server.start(1)
    tornado.ioloop.IOLoop.instance().start()