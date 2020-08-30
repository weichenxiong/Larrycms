from django.urls import path, include
from . import views

urlpatterns = [
    path("login/", views.login), # 登录
    path("index/", views.index),
    path("index/main/", views.main),
    path("index/company/", include("companyInfo.urls")), #公司详情
]


