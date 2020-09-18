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
        print(username, password)
        if len(username) > 0 and len(password) > 0:
            try:
                user = User.objects.get(username=username,password=password)
                request.session["username"] = username
                return redirect("/users/index/")
            except:
                return render(request, "login.html")
        else:
            return render(request, "login.html")
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