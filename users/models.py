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

def user_account_file_upload_path(instance, filename):
    return f'{instance.file_category}/{filename}'

class UserAccountFilePage(models.Model):
    class FileCategoryChoices(models.TextChoices):
        CV = "CV", "CV"
        REPORT = "REPORT", "REPORT"
        CERTIFICATE = "CERTIFICATE", "CERTIFICATE"

    user = models.ForeignKey(
        'users.UserAccount', models.CASCADE
    )
    file_category = models.CharField(max_length=20, choices=FileCategoryChoices.choices)
    
    file = models.FileField(upload_to=user_account_file_upload_path, blank=True, null=True) #TODO: delete blank=True, null=True
    # date_crated = models.DateField(blank=True, null=True)
    class Meta:
        verbose_name = "UserAccountFilePage"

class ReportModel(models.Model):

    report_file = models.OneToOneField(UserAccountFilePage, models.CASCADE, blank=True, null=True, related_name="report_file") #TODO: delete blank=True, null=True
    user_info = models.JSONField(blank=True, null=True) #TODO: delete blank=True, null=True
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
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True) #TODO: delete blank=True, null=True
    file_key = models.UUIDField(unique=True, editable=False, blank=True, null=True) #TODO: delete blank=True, null=True

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateField(auto_now_add=True)
    certificate_file = models.OneToOneField(UserAccountFilePage, models.CASCADE, blank=True, null=True, related_name="certificate_file") #TODO: delete blank=True, null=True
    file_key = models.UUIDField(unique=True, editable=False, blank=True, null=True) #TODO: delete blank=True, null=True

    class Meta:
        verbose_name = 'CertificateModel'
        verbose_name_plural = 'CertificateModels'
    
    def __str__(self) -> str:
        if self.certificate_file.user.email is not None:
            return self.certificate_file.user.email


class UniqueRandom(models.Model):
    user = models.ForeignKey('users.UserAccount', models.CASCADE, blank=True, null=True) #TODO: delete blank=True, null=True
    unique_value = models.CharField(max_length=32, unique=True)
    def __str__(self) -> str:
        return self.unique_value
    
    class Meta:
        verbose_name = 'UniqueRandom'
        verbose_name_plural = 'UniqueRandoms'
    
def user_file_upload_path(instance, filename):
    return f'user-files/{instance.user.email}/{instance.category}/{filename}'

class UserVerificationFile(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    category = models.CharField(max_length=150)
    file = models.FileField(upload_to=user_file_upload_path, null=True, blank=True) #TODO: delete blank=True, null=True

    class Meta:
        verbose_name = 'UserVerificationFile'
        verbose_name_plural = 'UserVerificationFiles'

