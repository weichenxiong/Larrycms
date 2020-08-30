from django.db import models


class User(models.Model):
    """用户模型"""
    nid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, verbose_name="用户名")
    password = models.CharField(max_length=20, verbose_name="密码")
    createTime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updateTime = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    iphone = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号")
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name="住址")
    
    class Meta:
        db_table = "LCMS_user"
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name