from django.urls import path
from . import views

urlpatterns = [
    path("detail/", views.CompanyInfoView.as_view()), #　公司详情
    path("structure/", views.DepartmentInfo.as_view()), # 公司部门展示
    path("department_action/", views.DepartmentAction.as_view()), # 部门的删除添加，删除
    path("export_excel/", views.downloadExcel), # 导出excel
    path('search/', views.SeachView), # 搜索功能
    path("department_edit/", views.DepartmentEdit.as_view()), # 部门编辑
    path("position/", views.Positions.as_view()), # 部门岗位
    path("del_user_position/", views.DelUserPosition), # 删除用户岗位
    path("export_position/", views.ExportUserPosition), #导出员工岗位信息
    path("batch_del/", views.BatchDelUserPosition), # 批量删除员工岗位
    path("add_user_position/" ,views.AddUserPosition), # 添加员工岗位
    path("user_position_edit/", views.UserPositionEdit.as_view()), # 编辑员工岗位信息
]