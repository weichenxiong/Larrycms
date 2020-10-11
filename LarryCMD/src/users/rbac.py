#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.conf import settings


class RbacMiddleware(MiddlewareMixin):
    """
    用户权限信息校验
    """
    def process_request(self, request):
        """
        当前用户请求进来时候执行
        """
        """
        1. 获取当前用户请求的URL
        2. 获取当用户在session中保存的URL列表
        3. 权限信息匹配
        """

        #针对login，admin等常用的路由设置白名单
        valid_url_list = [
            "/users/login/",
            "/admin/.*",
            "/users/loginout/",
        ]

        current_url = request.path_info
        # print(current_url,11111111111111111)
        for valid_url in valid_url_list:
            if re.match(valid_url, current_url):
                # 白名单中的URL无需进行权限验证，直接访问即可
                return None
                
        permission_list = request.session.get("permission_url_list_key")
        print(permission_list)
        if not permission_list:
            return HttpResponse("未获取用户权限信息，请重新登录！")
        
        flag = False

        for url in permission_list:
            # print(url, 22222222222222222)
            reg = "^%s$" % url
            if re.match(reg, current_url):
                flag = True
                break
        
        if not flag:
            return HttpResponse("无权访问！")
