import hashlib
import json
import time

import jwt
from django.conf import settings
from django.http import JsonResponse
from user.models import UserProfile


# Create your views here.
def tokens(request):
    """
        登录功能视图逻辑
        1.获取请求题的数据[用户名、密码]
        2.判断用户名是否存在
        3.判断密码是否正确
        4.签发token
        5.组织数据返回
    """
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    # 判断用户名
    try:
        user = UserProfile.objects.get(username=username)
    except Exception as e:
        print('get user error:', e)
        return JsonResponse({'code': 10200, 'error': 'username is wrong'})

    # 判断密码
    if user.password != hashlib.md5(password.encode()).hexdigest():
        return JsonResponse({'code': 10201, 'error': 'password is wrong'})

    # 签发token
    token = make_token(username)

    result = {
        'code': 200,
        'username': username,
        'data': {'token': token},
        'carts_count': 0
    }

    return JsonResponse(result)


def make_token(username, expire=24*3600):
    payload = {
        'exp': int(time.time()) + expire,
        'username': username
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
