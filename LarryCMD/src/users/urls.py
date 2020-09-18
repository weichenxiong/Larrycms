from django.urls import path, include
from . import views

urlpatterns = [
    path("login/", views.login), # 登录
    path("loginout/", views.loginout), # 退出
    path("index/", views.index),
    path("index/main/", views.main),
    path("index/company/", include("companyInfo.urls")), #公司详情
    path(r'search/', include('haystack.urls'), name='search'),
]


