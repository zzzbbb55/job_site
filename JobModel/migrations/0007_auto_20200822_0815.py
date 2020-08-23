# Generated by Django 3.1 on 2020-08-22 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobModel', '0006_job_item_interview_resume'),
    ]

    operations = [
        migrations.AddField(
            model_name='job_item',
            name='work_type',
            field=models.CharField(default='engineer', max_length=500),
        ),
        migrations.AddField(
            model_name='user',
            name='educational_background',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='user',
            name='expected_salary',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='user',
            name='gpa',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='user',
            name='professional_certificate',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='user',
            name='work_experience',
            field=models.CharField(default='', max_length=500),
        ),
    ]
