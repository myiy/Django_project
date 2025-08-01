from django.http import HttpResponse


def test_cors(request):
    """
    测试跨域
    """
    return HttpResponse('cors is ok')
