from django.urls import path
from . import views

urlpatterns = [
    # 注册功能
    path('', views.users),
]
