from django.db import models


class CompanyDetail(models.Model):
    company_name = models.CharField(max_length=50, verbose_name="公司名称")
    company_register = models.CharField(max_length=20, verbose_name="公司法人")
    business_license = models.CharField(max_length=50, verbose_name="营业执照")
    register_money = models.CharField(max_length=20, verbose_name="注册资金")
    company_address = models.CharField(max_length=50, verbose_name="公司地址")
    company_detail = models.CharField(max_length=1000, verbose_name="公司详情")

    class Meta:
        db_table = "LCMS_companydetail"
        verbose_name = "公司详情"
        verbose_name_plural = verbose_name   

class Department(models.Model):
    nid = models.AutoField(primary_key=True)
    number = models.CharField(max_length=11, verbose_name="编号")
    label = models.CharField(max_length=50, verbose_name="标签")
    department = models.CharField(max_length=20, verbose_name="部门名称")
    department_manager = models.ForeignKey("users.User", verbose_name="部门负责人",null=True, blank=True, on_delete=models.CASCADE)
    department_people = models.CharField(max_length=200, verbose_name="部门人数")
    create_time = models.DateField(verbose_name="创建时间")
    
    class Meta:
        db_table = "LCMS_companystructure"
        verbose_name = "部门信息"
        verbose_name_plural = verbose_name

class Position(models.Model):
    nid = models.AutoField(primary_key=True)
    position = models.CharField(max_length=15, verbose_name="岗位")

    class Meta:
        db_table = "LCMS_position"
        verbose_name = "岗位信息"
        verbose_name_plural = verbose_name

    

    