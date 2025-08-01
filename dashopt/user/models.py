from django.db import models


class UserProfile(models.Model):
    """
        用户表:用户名，密码，邮箱，手机号，是否激活，创建时间，更新时间
    """
    username = models.CharField('用户名', max_length=11, unique=True)
    password = models.CharField('密码', max_length=32)
    email = models.EmailField('邮箱')
    phone = models.CharField('手机号', max_length=11)
    is_active = models.BooleanField(default=False)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    # 修改表名
    class Meta:
        # 应用名_类名 非驼峰
        db_table = 'user_user_profile'
