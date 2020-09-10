from django.urls import path
from . import views

urlpatterns = [
    path("detail/", views.CompanyInfoView.as_view()), #　公司详情
    path("structure/", views.DepartmentInfo.as_view()), # 公司部门展示
    path("department_action/", views.DepartmentAction.as_view()), # 部门的删除添加，删除
    path("export_excel/", views.downloadExcel), # 导出excel
    path('search/', views.SeachView), # 搜索功能
    path("department_edit/", views.DepartmentEdit.as_view()), # 部门编辑
    path("position/", views.Position.as_view()), # 部门岗位
]