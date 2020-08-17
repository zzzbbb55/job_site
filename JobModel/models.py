from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=300)
    resume_url = models.CharField(max_length=500)

class recruiter(models.Model):
    company_name = models.CharField(max_length=30)
    password = models.CharField(max_length=300)
    info = models.CharField(max_length=500,default="")
    describe = models.CharField(max_length=500)
    user_type = models.CharField(max_length=100)

class job_item(models.Model):
    job_title = models.CharField(max_length=30)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    describe = models.CharField(max_length=100,default="")
    salary = models.CharField(max_length=100)
    requirement = models.CharField(max_length=500)
    received_resume = models.CharField(max_length=1000,default="")
    interview_resume = models.CharField(max_length=1000, default="")
    posted_date=models.DateTimeField(auto_now_add=True)