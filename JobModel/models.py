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