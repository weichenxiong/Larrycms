from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """用户模型"""
    nid = models.AutoField(primary_key=True)
    # username = models.CharField(max_length=20, verbose_name="用户名")
    # password = models.CharField(max_length=20, verbose_name="密码")
    enterTime = models.DateField(verbose_name="入职时间")
    leaveTime = models.DateField(verbose_name="离职时间")
    departments = models.ForeignKey("companyInfo.Department", verbose_name="部门", null=True, blank=True, on_delete=models.CASCADE)
    position = models.ForeignKey("companyInfo.Position", verbose_name="岗位", null=True, blank=True, on_delete=models.CASCADE)
    iphone = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号")
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name="住址")
    
    class Meta:
        db_table = "LCMS_user"
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name