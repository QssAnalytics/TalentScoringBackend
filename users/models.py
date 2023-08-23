import uuid

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
# Create your models here.
GENDER_CHOICES = (
    ("Female", "Female"),
    ("Male", "Male"),

)

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

class UserAccount(AbstractBaseUser):
    first_name = models.CharField(max_length = 150, null=True, blank = True)
    last_name = models.CharField(max_length = 150, null=True, blank = True)
    email = models.EmailField(unique=True, blank=True, null=True)
    birth_date = models.DateField( blank=True, null=True)
    gender = models.CharField(max_length=10, choices = GENDER_CHOICES, blank=True, null=True)
    native_language = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    user_info = models.JSONField(blank=True, null=True)
    test = models.CharField(max_length = 150, null=True, blank = True)
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    
    class Meta:
        verbose_name = "UserAccount"
        verbose_name_plural = "UserAccounts"


    def has_perm(self, perm, obj=None):
      return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser    
    def __str__(self):
        
        return self.email


class ReportModel(models.Model):
    user = models.ForeignKey(
        'users.UserAccount', models.CASCADE
    )
    user_info = models.JSONField(blank=True, null=True)
    education_score = models.DecimalField(max_digits=16, decimal_places=13)
    education_color = models.CharField(max_length=30, default='#00E5BC')
    language_score = models.DecimalField(max_digits=16, decimal_places=13)
    language_color = models.CharField(max_length=30, default='#FF0038')
    special_skills_score = models.DecimalField(max_digits=16, decimal_places=13)
    special_skills_color = models.CharField(max_length=30, default='#00A8E1')
    sport_score = models.DecimalField(max_digits=16, decimal_places=13)
    sport_color = models.CharField(max_length=30, default='#09959A')
    work_experiance_score = models.DecimalField(max_digits=16, decimal_places=13)
    work_experiance_color = models.CharField(max_length=30, default='#FFCB05')
    program_score = models.DecimalField(max_digits=16, decimal_places=13)
    program_color = models.CharField(max_length=30, default='#8800E0')

    report_file = models.FileField(upload_to='images/', blank=True, null=True)

    class Meta:
        verbose_name = "ReportModel"
        

    def __str__(self) -> str:
        return self.user.email 
    
    def delete(self,*args,**kwargs):
        self.report_file.delete(save=False)
        super().delete(*args, **kwargs)


class UserCV(models.Model):
    pass
class CertificateModel(models.Model):
    user = models.ForeignKey(
        'users.UserAccount', models.CASCADE
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    cert_file = models.FileField(upload_to='certificate/', blank=True, null=True)
    cert_image = models.FileField(upload_to='certificate/images', blank=True, null=True)

    class Meta:
        verbose_name = 'Certificate Model'
        verbose_name_plural = 'Certificate Model'
    
    def __str__(self) -> str:
        return self.user.email
    

class CertificateModel(models.Model):
    user = models.ForeignKey(
        'users.UserAccount', models.CASCADE
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    cert_file = models.FileField(upload_to='certificate/', blank=True, null=True)
    cert_image = models.FileField(upload_to='certificate/images', blank=True, null=True)

    class Meta:
        verbose_name = 'Certificate Model'
        verbose_name_plural = 'Certificate Model'
    
    def __str__(self) -> str:
        return self.user.email
    
class UserCV(models.Model):
    pass