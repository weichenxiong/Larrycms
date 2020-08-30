from django.shortcuts import render, redirect, HttpResponse
from .models import User


def login(request):
    """登录"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if len(username) > 0 and len(password) > 0:
            try:
                user = User.objects.get(username=username,password=password)
                print("ok")

                return redirect("/users/index/")
            except:
                print("no")
                return render(request, "login.html")
        else:
            return render(request, "login.html")
    return render(request, "login.html")

def loginout(request):
    """退出"""
    pass

def index(request):
    return render(request, "index.html")

def main(request):
    return render(request, "main.html")

def companydetails(request):
    return render(request, "companydetails.html")