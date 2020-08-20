import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from JobModel.models import User, job_item, recruiter
from job_site.settings import BASE_DIR


def hello(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return redirect(reverse("index"))

def get_user_name_and_type(request_obj):
    context = {}
    if "user" in request_obj.session and "name" in request_obj.session["user"] and "user_type" in request_obj.session["user"]:
            print("user access index page:" + request_obj.session["user"]["name"])
            context['username'] = request_obj.session["user"]["name"]
            context['user_type'] = request_obj.session["user"]["user_type"]
            
    else:
        print("guest access index page")
        context['username'] = "logout"
        context['user_type'] = "logout"
    return context


def index(request):
    context =  get_user_name_and_type(request)
    job_list = job_item.objects.all().order_by("posted_date").reverse()
    display_job_list = list()
    for each_job in job_list:
        try:
            display_job_list.append({"id":each_job.id,
                                     "job_title": each_job.job_title,
                                     "company":each_job.company,
                                     "location":each_job.location,
                                     "salary":each_job.salary,
                                     "requirements":each_job.requirement,
                                     "received_resume":each_job.received_resume,
                                     "data":each_job.posted_date.strftime("%Y-%m-%d")})
        except Exception as e:
            print(e)
    context["display_job_list"] = display_job_list
    return render(request, 'index.html', context)

def job_details(request,job_id):
    context = get_user_name_and_type(request)
    if context["username"] == "logout":
            return redirect(reverse("login_page"))
    each_job = job_item.objects.get(id=job_id)
    context["job"]={"id":each_job.id,
                 "job_title": each_job.job_title,
                 "company":each_job.company,
                 "location":each_job.location,
                 "salary":each_job.salary,
                 "requirements":each_job.requirement,
                 "received_resume":each_job.received_resume,
                 "data":each_job.posted_date.strftime("%Y-%m-%d")}
    return render(request, 'job_details_page.html', context)

def my_resume(request):
    return render(request, 'dashboard.html', )

def recruiter_page(request):
    context =  get_user_name_and_type(request)
    job_list = job_item.objects.filter(company=context["username"]).order_by("posted_date").reverse()
    display_job_list = list()
    received_resume_list = list()
    for each_job in job_list:
        try:
            if each_job.received_resume != "":
                sent_user_list = each_job.received_resume.split("/")
                for each_user in sent_user_list:
                    if each_user != "" and each_user != " " :
                        user_resume = User.objects.get(username=each_user).resume_url
                        received_resume_list.append({"user":each_user,
                                                     "job":each_job.job_title,
                                                     "job_id":each_job.id,
                                                     "interview_resume": each_job.interview_resume,
                                                     "user_resume": user_resume})
            display_job_list.append({"id":each_job.id,
                                     "job_title": each_job.job_title,
                                     "company":each_job.company,
                                     "location":each_job.location,
                                     "salary":each_job.salary,
                                     "requirements":each_job.requirement,
                                     "received_resume":each_job.received_resume,
                                     "interview_resume": each_job.interview_resume,
                                     "data":each_job.posted_date.strftime("%Y-%m-%d")})
        except Exception as e:
            print(e)
    context["display_job_list"] = display_job_list
    context["received_resume_list"] = received_resume_list
    return render(request, 'recruiter_page.html', context)

def dashboard(request):
    context =  get_user_name_and_type(request)
    username = context["username"]
    usertype = context["user_type"]
    if usertype == "candidate":
        job_list = job_item.objects.filter(interview_resume__contains=username).order_by("posted_date").reverse()
        sent_resume_list = job_item.objects.filter(received_resume__contains=username).order_by("posted_date").reverse()
        interview_list = []
        sent_record = []
        for job in job_list:
            interview_list.append({"job_id":job.id,
                                   "job_title":job.job_title,
                                   "company":job.company})
        for job in sent_resume_list:
            sent_record.append({"job_id":job.id,
                                 "job_title":job.job_title,
                                 "company":job.company})
        context["interview_list"] = interview_list
        context["len_interview_list"] = len(interview_list)
        context["sent_record"] = sent_record
        context["len_sent_record"] = len(sent_record)
        query_user = User.objects.filter(username=username)[0]
        user_resume_url = query_user.resume_url
        context["resume_url"] = user_resume_url
    elif usertype == "recruiter":
        query_company = recruiter.objects.filter(company_name=username)[0]
        context["company_name"] = query_company.company_name
        context["company_info"] = query_company.info
        context["company_describe"] = query_company.describe
    else:
        return redirect(reverse("login_page"))
    
    return render(request, 'dashboard.html',context )

def login_page(request):
    return render(request, 'login_page.html', )

def register_page(request):
    return render(request, 'register_page.html', )

def user_login(request):
    try:
        if request.POST:
            request.encoding='utf-8'
            if 'username' in request.POST and request.POST['username']:
                username = request.POST['username']
                if 'password' in request.POST and request.POST['password']:
                    password = request.POST['password']
                    message = ""
                else:
                    raise Exception('error: empty password')
            else:
                 raise Exception('error: empty user name')
            query_user = User.objects.filter(username=username)
            query_company = recruiter.objects.filter(company_name=username)
            if len(query_user) >= 1:
                user_type = "candidate"
                query_list = query_user
            elif len(query_company) >= 1:
                user_type = "recruiter"
                query_list = query_company
            else:
                raise Exception("error: user not existed, please register.")  
            if query_list[0].password == password:
                request.session['user'] = {}
                request.session['user']["name"] = username
                request.session['user']["user_type"] = user_type
            else:
                raise Exception("error: wrong password")  
            
            if user_type == "recruiter":
                return redirect("/message/ok/%s_has_login/recruiter_page/" % username.replace(" ","_"))
            else:
                return redirect("/message/ok/%s_has_login/index/" % username.replace(" ","_"))

                
        else:
            raise Exception("not support get")
    except Exception as e:
        message= str(e)
        message = message.replace(" ","_")
        return redirect("/message/error/%s/login/" % message)

def user_logout(request):
    if "user" in request.session:
        request.session.pop("user")
    return redirect("/message/ok/user_has_logout/index/")

def user_register(request):
    # if request.POST:
    try:
        massage = "pass"
        print (request.POST["people_type"])
        if "/" in request.POST["username"]:
            raise Exception("error : illegal character '/' ")
        if request.POST["people_type"] == "candidate":
            username = request.POST["username"]
            if request.POST["password"] == request.POST["password_confirm"]:
                password = request.POST["password"]
                if len(User.objects.filter(username=username)) == 0 and len(recruiter.objects.filter(company_name=username)) == 0:
                    new_user = User(username=username,password=password,resume_url="")
                    new_user.save()
                else:
                    raise ( "error : user existed, please login")
            else:
                raise ( "error : password is not same as password_confirm")
        else:
            company_name = request.POST["username"]
            
            company_location = request.POST["company_location"]
            company_description = request.POST["company_description"]
            if request.POST["password"] == request.POST["password_confirm"]:
                password = request.POST["password"]
                if len(recruiter.objects.filter(company_name=company_name)) == 0 and len(User.objects.filter(username=company_name)) == 0:
                    new_company = recruiter(company_name=company_name,password=password,info=company_location,describe=company_description,user_type="recruiter")
                    new_company.save()
                else:
                    raise ( "error : company existed, please login")
            else:
                raise ( "error : password is not same as password_confirm")
        return redirect("/message/ok/user_has_been_added/login/" )
    except Exception as e:
        message = str(e)
        message = message.replace(" ","_")
        return redirect("/message/error/%s/register/" % message)
        

def add_job(request):
    if request.POST:
        if "job_title" in request.POST and\
            "company" in request.POST and\
            "location" in request.POST and\
            "salary" in request.POST and\
            "requirements" in request.POST:
            job_title = request.POST["job_title"]
            company = request.POST["company"]
            location = request.POST["location"]
            salary = request.POST["salary"]
            requirement = request.POST["requirements"]
            new_job = job_item(job_title=job_title,company=company,location=location,salary=salary,requirement=requirement,describe="hash_"+str(hash(request)))
            new_job.save()
        else:
            return redirect("/message/error/please_fiil_up_all_args/dashboard/")
            # raise Exception("please fiil up or args")
        return redirect("/message/ok/job_has_added/dashboard/")

def delete_job(request):
    if request.POST:
        if "job_id" in request.POST :
            job_id = request.POST["job_id"]
            new_job = job_item.objects.get(id=job_id)
            new_job.delete()
        else:
            return redirect("/message/error/please_fiil_up_all_args/recruiter_page/")
            # raise Exception("please fiil up or args")
        return redirect("/message/ok/job_has_deleted/recruiter_page/")


def send_resume(request):

    if "username" not in request.POST or request.POST["username"] == "logout":
            return redirect(reverse("login_page"))
    elif User.objects.get(username=request.POST["username"]).resume_url == "":
        return redirect("/message/No_Resume/please_go_to_dashboard_to_upload_your_resume/dashboard/")
    if request.POST:
        
        job_id = request.POST["job_id"]
        username = request.POST["username"]
        job = job_item.objects.get(id=job_id)
        now_data = job.received_resume
        job.received_resume = now_data + '/' + username
        job.save()
        return redirect("/index/#jobcard%s" % job_id)


def send_invite(request):
    if request.POST["username"] == "logout":
        return redirect(reverse("login_page"))

    if request.POST:
        job_id = request.POST["job_id"]
        username = request.POST["username"]
        job = job_item.objects.get(id=job_id)
        now_data = job.interview_resume
        job.interview_resume = now_data + '/' + username
        job.save()
        return redirect("/recruiter_page/#received")

def message_page(request,title,message,redirect_url):
    context          = {}
    context['title'] = title
    context['message'] = message.replace("_"," ")
    context['redirect_url'] = redirect_url
    return render(request, 'message.html', context)

def upload_file(request):
    user_info = get_user_name_and_type(request)
    if user_info["username"] == "logout":
        raise Exception("No user info")
    myFile = request.FILES.get("myfile", None)
    if not myFile:
        return redirect("/message/error/No_file_was_Selected!/dashboard/")
    destination = open(os.path.join(BASE_DIR, "statics", "files", myFile.name), 'wb+')
    for chunk in myFile.chunks():
        destination.write(chunk)
    destination.close()

    User1 = User.objects.get(username=user_info["username"])
    User1.resume_url = myFile.name
    User1.save()
    return redirect("/message/ok/File_has_uploaded_!/dashboard/")