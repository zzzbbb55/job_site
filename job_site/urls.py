"""job_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from . import views
urlpatterns = [
    path("", views.hello, name='empty'),
    re_path(r'^index/$', views.index, name='index'),
    re_path(r'^my_resume/$', views.my_resume, name='resume'),
    re_path(r'^recruiter_page/$', views.recruiter_page, name='recruiter_page'),
    re_path(r'^account/$', views.account, name='account'),
    re_path(r'^login/$', views.login_page, name='login_page'),
    re_path(r'^register/$', views.register_page, name='register_page'),
    re_path(r'^user_login/$', views.user_login, name='user_login'),
    re_path(r'^user_logout/$', views.user_logout, name='user_logout'),
    re_path(r'^user_register/$', views.user_register, name='user_register'),
    re_path(r'^send_resume/$', views.send_resume, name='send_resume'),
    re_path(r'^add_job/$', views.add_job, name='add_job'),
    re_path(r'^delete_job/$', views.delete_job, name='delete_job'),
    re_path(r'^send_invite/$', views.send_invite, name='send_invite'),
    re_path(r'^upload_file/$', views.upload_file, name='upload_file'),
    re_path(r'^change_info/$', views.change_info, name='change_info'),
    re_path(r'^test/$', views.test, name='test'),
    path('job_details/<job_id>/', views.job_details, name='job_details'),
    path('message/<title>/<message>/<redirect_url>/', views.message_page, name='message_page'),
]
