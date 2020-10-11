from django.db import models
from django.contrib.auth.models import AbstractUser


class Permission(models.Model):
    """权限表"""
    title = models.CharField(verbose_name="标题", max_length=32)
    url = models.CharField(verbose_name="含正则的URL", max_length=128)
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = "LCMS_permission"
        verbose_name = "权限信息"
        verbose_name_plural = verbose_name

class Role(models.Model):
    """
    角色表
    """
    title = models.CharField(verbose_name='角色名称', max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "LCMS_role"
        verbose_name = "角色信息"
        verbose_name_plural = verbose_name

class User(AbstractUser):
    """用户模型"""
    nid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, verbose_name="用户名", unique=True)
    # password = models.CharField(max_length=20, verbose_name="密码")
    enterTime = models.DateField(verbose_name="入职时间", null=True, blank=True)
    leaveTime = models.DateField(verbose_name="离职时间", null=True, blank=True)
    departments = models.ForeignKey("companyInfo.Department", verbose_name="部门", null=True, blank=True, on_delete=models.CASCADE)
    position = models.ForeignKey("companyInfo.Position", verbose_name="岗位", null=True, blank=True, on_delete=models.CASCADE)
    iphone = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号")
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name="住址")
    roles = models.ManyToManyField(verbose_name='拥有的所有角色', to='Role', blank=True)

    class Meta:
        db_table = "LCMS_user"
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name