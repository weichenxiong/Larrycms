from django.urls import path
from . import views

urlpatterns = [
    path("detail/", views.CompanyInfoView.as_view()), #　公司详情
    path("structure/", views.DepartmentInfo.as_view()), # 公司架构
    path("department_action/", views.DepartmentAction.as_view()), # 部门的编辑，删除
    path("export_excel/", views.downloadExcel), # 导出excel
    path('search/', views.SeachView),
]