from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'index.html', context)

def my_resume(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'resume.html', context)