from django.shortcuts import render, redirect, HttpResponse
from .models import User

# 登录装饰器
def auth(func):
    def inner(request, *args, **kwargs):
        if request.session.get("username"):
            return func(request, *args, **kwargs)
        else:
            return redirect("/users/login/")
    return inner


def login(request):
    """登录"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        current_user = User.objects.filter(username=username, password=password).first()
        if not current_user:
            return render(request, 'login.html', {'msg': '用户名或密码错误'})
        
        # 根据当前用户获取所有权限，并存入session中
        permission_queryset = current_user.roles.filter(permissions__isnull=False).values("permissions__id",
                                                                                    "permissions__url",
                                                                                    ).distinct()

        # 获取权限中的所有URL
        permission_list = list()
        for item in permission_queryset:
            # print(item["permissions__url"])
            permission_list.append(item["permissions__url"])
        # 用户的URL存进session中
        request.session["permission_url_list_key"] = permission_list
        # session保存登录信息
        request.session["username"] = username
        return redirect("/users/index/")

    #     print(username, password)
    #     if len(username) > 0 and len(password) > 0:
    #         try:
    #             user = User.objects.get(username=username,password=password)
    #             request.session["username"] = username
    #             return redirect("/users/index/")
    #         except:
    #             return render(request, "login.html")
    #     else:
    #         return render(request, "login.html")
    return render(request, "login.html")

def loginout(request):
    request.session["username"] = ""
    return redirect("/users/login/")
    pass

@auth
def index(request):
    return render(request, "index.html")

@auth
def main(request):
    return render(request, "main.html")

@auth
def companydetails(request):
    return render(request, "companydetails.html")