from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from JobModel.models import User

def hello(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return redirect(reverse("index"))

def index(request):
    context          = {}
    # request.session["username"] = "haha"
    if "username" in request.session:
        print("user access index page:" + request.session["username"])
        context['username'] = request.session["username"]
    else:
        print("guest access index page")
        context['username'] = "logout"
    return render(request, 'index.html', context)

def my_resume(request):
    return render(request, 'dashboard.html', )

def recruiter_page(request):
    return render(request, 'recruiter_page.html', )

def dashboard(request):
    return render(request, 'dashboard.html', )

def login_page(request):
    return render(request, 'login_page.html', )

def register_page(request):
    return render(request, 'register_page.html', )

def user_login(request):
    request.encoding='utf-8'
    if 'username' in request.GET and request.GET['username']:
        username = request.GET['username']
        if 'password' in request.GET and request.GET['password']:
            password = request.GET['password']
            message = ""
        else:
            message = 'error: empty password'    
    else:
        message = 'error: empty user name'
    if "error" not in message:
        query_user = User.objects.filter(username=username)
        if len(query_user) == 0:
            message = "error: user not existed, please register."
        else:
            if query_user[0].password == password:
                message = "pass"
                request.session['username'] = username
            else:
                message = "error: wrong password"
    
    if message == "pass":
        return redirect(reverse("index"))
    else:
        return HttpResponse(message)

def user_logout(request):
    if "username" in request.session:
        request.session.pop("username")
    return redirect(reverse("index"))