# Generated by Django 4.1.7 on 2023-08-03 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_question_options_remove_useraccount_age'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccount',
            name='username',
        ),
        migrations.AddField(
            model_name='useraccount',
            name='birth_date',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='gender',
            field=models.CharField(blank=True, choices=[('Female', 'Female'), ('Male', 'Male')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='native_language',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]