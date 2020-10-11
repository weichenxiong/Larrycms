import json
import xlwt
import datetime
from io import BytesIO
from django.shortcuts import render, redirect,HttpResponse
from django.views import View
from .models import CompanyDetail, Department, Position
from users.models import User
from django.http import HttpResponseRedirect
from haystack.views import SearchView
from users.views import auth
from django.utils.decorators import method_decorator


@method_decorator(auth, name="get")
@method_decorator(auth, name="post")
class CompanyInfoView(View):
    """公司详情"""
    def get(self, request):
        # 展示数据
        templates_name = "companydetails.html"
        companyInfo = CompanyDetail.objects.all()

        return render(request, templates_name, {"companyInfo": companyInfo})

    def post(self, request):
        # 获取前端返回的数据
        url = "/users/index/company/detail"
        company_name = request.POST.get("companyName")
        username = request.POST.get("username")
        companyID = request.POST.get("companyID")
        register_money = request.POST.get("register_money")
        address = request.POST.get("address")          
        detail = request.POST.get("detail")
        print(company_name, username, companyID, register_money, address, detail)
        # 保存数据
        CompanyDetail.objects.update(company_name=company_name, company_register=username,business_license=companyID, register_money=register_money, company_address=address, company_detail=detail)

        return redirect(url)


@method_decorator(auth, name="get")
@method_decorator(auth, name="post")
class DepartmentInfo(View):
    """公司架构"""
    def get(self, request):

        templates_name = "department.html"
        dataList = Department.objects.all()
        userList = User.objects.all()
        return render(request, templates_name,locals())

    def post(self, request):
        pass

@method_decorator(auth, name="get")
@method_decorator(auth, name="post")      
@method_decorator(auth, name="delete") 
class DepartmentAction(View):

    def get(self, request):
        #　删除部门
        url = "/users/index/company/structure/"
        nid = request.GET.get("nid")
        Department.objects.filter(nid=nid).delete()

        return redirect(url)
        
    def post(self, request):
        # 添加部门
        url = "/users/index/company/structure/"

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
        
        return redirect(url)
        
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

@auth
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
        print(data)
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

@method_decorator(auth, name="extra_context")
class SeachView(SearchView):
    """搜索功能"""
    def extra_context(self):       #重载extra_context来添加额外的context内容
        context = super(MySeachView,self).extra_context()
        side_list = Topic.objects.filter(kind='major').order_by('add_date')[:8]
        context['side_list'] = side_list
        return context

@method_decorator(auth, name="get")
@method_decorator(auth, name="post")
class DepartmentEdit(View):
    """部门编辑"""
    def get(self, request):

        templates_name = "department_edit.html"
        nid = request.GET.get("nid")
        userList = User.objects.all()
        data = Department.objects.filter(nid=nid).first()

        return render(request, templates_name, locals())

    def post(self, request):

        url = "/users/index/company/structure/"
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

        return redirect(url)

@method_decorator(auth, name="get")
@method_decorator(auth, name="post")
class Positions(View):
    """员工岗位"""
    def get(self, request):
        '''获取数据展示'''
        templates_name = "position.html"
        userList = User.objects.all()
        positionList = Position.objects.all()
        departmentList = Department.objects.all()
        # for i in data:
        #     print(i.username, i.departments, i.position)
        return render(request, templates_name, locals())
    
    def post(self,request):
        pass


@auth
def DelUserPosition(request):
    """删除用户岗位"""
    url = "/users/index/company/position/"

    if request.method == "GET":
        nid = request.GET.get("nid")
        User.objects.filter(nid=nid).delete()
        return redirect(url)

@auth
def ExportUserPosition(request):
    """导出员工岗位信息"""
    if request.method == "POST":
        # 创建一个表
        wb = xlwt.Workbook(encoding="utf8")
        # 创建一个sheet对象
        sheet = wb.add_sheet("position")
        # 写入标题数据
        sheet.write(0, 0, "序号")
        sheet.write(0, 1, "姓名")
        sheet.write(0, 2, "岗位")
        sheet.write(0, 3, "部门")
        sheet.write(0, 4, "入职时间")
        sheet.write(0, 5, "离职时间")
        sheet.write(0, 6, "电话")
        sheet.write(0, 7, "住址")

        data = User.objects.all()
        data = list(data)
        excel_row = 1
        for i in range(len(data)):
            sheet.write(excel_row, 0, data[i].nid)
            sheet.write(excel_row, 1, data[i].username)
            sheet.write(excel_row, 2, data[i].position.position)
            sheet.write(excel_row, 3, data[i].departments.department)
            sheet.write(excel_row, 4, data[i].enterTime)
            sheet.write(excel_row, 5, data[i].leaveTime)
            sheet.write(excel_row, 6, data[i].iphone)
            sheet.write(excel_row, 7, data[i].address)
            excel_row += 1
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

@auth
def BatchDelUserPosition(request):
    """批量删除选中的记录"""
    dataList = list()
    data = json.loads(request.body)["value"]
    for i in data:
        dataList.append(int(i))
    User.objects.filter(nid__in=dataList).delete() #进行批量删除
    return HttpResponse("ok")

@auth 
def AddUserPosition(request):
    """添加员工"""
    url = "/users/index/company/position/"
    
    username = request.POST.get("username")
    password = request.POST.get("password")
    position = request.POST.get("position")
    department = request.POST.get("department")
    enterTime = request.POST.get("enterTime")
    leaveTime = request.POST.get("leaveTime")
    iphone = request.POST.get("iphone")
    address = request.POST.get("address")
    #todo  数据验证
    User.objects.create(username=username, password=password, position_id=position,departments_id=department,
                        enterTime=enterTime,leaveTime=leaveTime,iphone=iphone,address=address)
    print(username, position,department,enterTime,leaveTime,iphone,address)
    return redirect(url)

@method_decorator(auth, name="get")
@method_decorator(auth, name="post")
class UserPositionEdit(View):
    def get(self,request):

        templates_name = "position_edit.html"
        nid = request.GET.get("nid")
        userList = User.objects.filter(nid=nid).first()
        positionList = Position.objects.all()
        departmentList = Department.objects.all()
        return render(request, templates_name, locals())
        

    def post(self, request):
        
        url = "/users/index/company/position/"
        nid = request.POST.get("nid")
        username = request.POST.get("username")
        password = request.POST.get("password")
        position = request.POST.get("position")
        department = request.POST.get("department")
        enterTime = request.POST.get("enterTime")
        leaveTime = request.POST.get("leaveTime")
        iphone = request.POST.get("iphone")
        address = request.POST.get("address")
        print(nid,username,password, position,department,enterTime,leaveTime,iphone,address)
        User.objects.filter(nid=nid).update(username=username, password=password,position_id=position,departments_id=department,
                            enterTime=enterTime,leaveTime=leaveTime,iphone=iphone,address=address)
        return redirect(url)