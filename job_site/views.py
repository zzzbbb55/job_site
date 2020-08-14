from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse


def hello(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return redirect(reverse("index"))

def index(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'index.html', context)

def my_resume(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'dashboard.html', context)

def recruiter_page(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'recruiter_page.html', context)

def dashboard(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'dashboard.html', context)

def login(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'login_page.html', context)

def register(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'register_page.html', context)