import json
import xlwt
from io import BytesIO
from django.shortcuts import render, redirect,HttpResponse
from django.views import View
from .models import CompanyDetail, Department
from users.models import User
from django.http import HttpResponseRedirect
from haystack.views import SearchView


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

def downloadExcel(request):
    """导出excel"""
    if request.method == "POST":
        #　创建一个表
        wb = xlwt.Workbook(encoding="utf8")
        #　创建一个sheet对象，名字为department
        sheet = wb.add_sheet("department")
        #写入文件标题
        sheet.write(0, 0, "序号")
        sheet.write(0, 1, "编号")
        sheet.write(0, 2, "标签")
        sheet.write(0, 3, "部门名称")
        sheet.write(0, 4, "负责人")
        sheet.write(0, 5, "部门人数")
        sheet.write(0, 6, "创建时间")

        data = Department.objects.all()
        data = list(data)
        excel_row = 1
        for i in range(len(data)):
            sheet.write(excel_row, 0, data[i].nid)
            sheet.write(excel_row, 1, data[i].number)
            sheet.write(excel_row, 2, data[i].label)
            sheet.write(excel_row, 3, data[i].department)
            sheet.write(excel_row, 4, data[i].department_manager.username)
            sheet.write(excel_row, 5, data[i].department_people)
            sheet.write(excel_row, 6, data[i].create_time)
            excel_row += 1
            print(data[i].nid, data[i].number, data[i].label, data[i].department, data[i].department_manager.username)
        # 写到io
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        #　设置HTTPResponse的类型
        response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=test.xls'
        response.write(output.getvalue())
        print("创建成功",response)
        return response


class SeachView(SearchView):
    """搜索功能"""
    def extra_context(self):       #重载extra_context来添加额外的context内容
        context = super(MySeachView,self).extra_context()
        side_list = Topic.objects.filter(kind='major').order_by('add_date')[:8]
        context['side_list'] = side_list
        return context

class DepartmentEdit(View):
    def get(self, request):
        templates_name = "department_edit.html"
        nid = request.GET.get("nid")
        userList = User.objects.all()
        data = Department.objects.filter(nid=nid).first()

        return render(request, templates_name, locals())

    

    def post(self, request):
        nid = request.POST.get("nid")
        number = request.POST.get("number")
        label = request.POST.get("label")
        department = request.POST.get("department")
        department_manager = request.POST.get("user")
        department_people = request.POST.get("department_people")
        create_time = request.POST.get("create_time")
        print(nid,number, label, Department, department_manager, department_people, create_time)
        Department.objects.filter(nid=nid).update(number=number, label=label, department=department,
            department_manager_id=department_manager, department_people=department_people,
            create_time=create_time)
        return redirect("/users/index/company/structure/")

