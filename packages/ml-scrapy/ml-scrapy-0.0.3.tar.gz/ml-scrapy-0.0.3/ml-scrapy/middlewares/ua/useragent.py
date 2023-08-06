# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       ua
   Description:     User-Agent中间件
   Author:          MicLon
   date:            2021/8/30
-------------------------------------------------
"""
from .ua_list import ua_list


class UserAgentMiddleware:

    def __init__(self):
        ...

    def process_request(self, request, spider):
        random_ua = ua_list()
        if random_ua:
            request.headers.setdefault('User-Agent', random_ua)