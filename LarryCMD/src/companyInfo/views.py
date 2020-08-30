import json
from django.shortcuts import render, redirect,HttpResponse
from django.views import View
from .models import CompanyDetail, Department
from users.models import User
from django.http import HttpResponseRedirect

class CompanyInfoView(View):
    """公司详情"""
    def get(self, request):
        # 展示数据
        companyInfo = CompanyDetail.objects.all()
        # for company in companyInfo:
        #     print(company.company_name)
        return render(request, "companydetails.html", {"companyInfo": companyInfo})

    def post(self, request):
        # 获取前端返回的数据
        company_name = request.POST.get("companyName")
        username = request.POST.get("username")
        companyID = request.POST.get("companyID")
        register_money = request.POST.get("register_money")
        address = request.POST.get("address")          
        detail = request.POST.get("detail")
        print(company_name, username, companyID, register_money, address, detail)
        # 保存数据
        CompanyDetail.objects.update(company_name=company_name, company_register=username,business_license=companyID, register_money=register_money, company_address=address, company_detail=detail)

        return redirect("/users/index/company/detail")

class DepartmentInfo(View):
    """公司架构"""
    def get(self, request):
        dataList = Department.objects.all()
        userList = User.objects.all()
        return render(request, "department.html",locals())

    def post(self, request):
        pass
        
class DepartmentAction(View):
    def get(self, request):
        #　删除部门
        nid = request.GET.get("nid")
        Department.objects.filter(nid=nid).delete()

        return redirect("/users/index/company/structure/")
        
    def post(self, request):
        # 添加部门
        number = request.POST.get("number")
        label = request.POST.get("label")
        department = request.POST.get("department")
        department_manager = request.POST.get("user")
        department_people = request.POST.get("department_people")
        create_time = request.POST.get("create_time")
        print(number, label, department, department_manager, department_people, create_time)
        ret = Department.objects.create(number=number, label=label,department=department,
                department_manager_id = department_manager,
                department_people=department_people,create_time=create_time)
        
        return redirect("/users/index/company/structure/")
        
    def delete(self, request):
        # 批量删除部门
        dataList = list()   
        data = json.loads(request.body)["value"]
        for i in data:
            dataList.append(int(i))
        print(dataList)
        Department.objects.filter(nid__in=dataList).delete() # 进行批量删除
        # 这里不应该使用Httpresponse的，用其他进行页面刷新或者跳转就会被跨域限制，只能在前段进行页面刷新
        return HttpResponse("ok")
 
        

