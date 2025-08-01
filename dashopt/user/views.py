import hashlib
import json
import time

import jwt
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from user.models import UserProfile


# Create your views here.
def users(request):
    """
    注册功能逻辑视图
    1.获取请求体数据[request.body-字节串格式]
    2.数据校验[不做]
    3.检查用户名是否存在
        3.1 已存在：直接返回错误代码
        3.2 不存在：处理密码，存入数据表
    4.生成token
    5.返回正确响应[看接口文档]
    """

    # 获取请求体数据
    data = json.loads(request.body)
    uname = data.get('uname')
    password = data.get('password')
    phone = data.get('phone')
    email = data.get('email')

    # 数据库查询
    old_users = UserProfile.objects.filter(username=uname)
    # 用户已存在
    if old_users:
        return JsonResponse({'code': 10100, 'error': 'The username is existed'})

    # 存入数据库
    try:
        user = UserProfile.objects.create(
            username=uname,
            password=hashlib.md5(password.encode()).hexdigest(),      # 密码进行加密
            phone=phone,
            email=email
        )
    except Exception as e:
        print(e)
        return JsonResponse({'code': 10101, 'error': 'The username is existed'})

    # 签发token
    token = make_token(uname)

    # 组织数据返回
    result = {
        'code': 200,
        'username': uname,
        'data': {'token': token},
        'carts_count': 0
    }

    return JsonResponse(result)


def make_token(uname, expire=3600*24):
    """生成token"""
    payload = {
        'exp': int(time.time()) + expire,
        'username': uname,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')



