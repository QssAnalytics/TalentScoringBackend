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
    cert_unique_key = models.CharField(max_length=32, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Certificate Model'
        verbose_name_plural = 'Certificate Model'
    
    def __str__(self) -> str:
        return self.user.email


class UniqueRandom(models.Model):
    unique_value = models.CharField(max_length=32, unique=True)
    def __str__(self) -> str:
        return self.unique_value

class FileCategory(models.Model):
    name = models.CharField(max_length=50)
    file_count = models.PositiveIntegerField(default=0, editable=False)  # Field to store the file count
    allows_multiple_files = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

def user_file_upload_path(instance, filename):
    return f'user-files/{instance.user.email}/{instance.category.name}/{filename}'

class UserFile(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    category = models.ForeignKey(FileCategory, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_file_upload_path, null=True, blank=True)
    
    class Meta:
        verbose_name = 'User File'
        verbose_name_plural = 'User Files'
    
    def __str__(self):
        return f"{self.user.email} - {self.category}"
    
    def save(self, *args, **kwargs):
        # Increment the file count for the category when a new UserFile is created
        if not self.pk: 
            self.category.file_count += 1
            self.category.save()
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Decrement the file count for the category when a UserFile is deleted
        self.category.file_count -= 1
        self.category.save()
        super().delete(*args, **kwargs)

# class UserFiles(models.Model):
#     user = models.ForeignKey('users.UserAccount', models.CASCADE)
#     passport = models.FileField(upload_to='user-files/passports/', blank=True, null=True)
#     attestat9 = models.FileField(upload_to='user-files/attestat9/', blank=True, null=True)
#     attestat11 = models.FileField(upload_to='user-files/attestat11/', blank=True, null=True)
#     student_card = models.FileField(upload_to='user-files/student-cards/', blank=True, null=True)
#     bachelor_diplom = models.FileField(upload_to='user-files/diplom/bachelor/', blank=True, null=True)
#     master_diplom = models.FileField(upload_to='user-files/diplom/master/', blank=True, null=True)
#     phd_diplom = models.FileField(upload_to='user-files/diplom/phd/', blank=True, null=True)
#     olimp_sened = models.FileField(upload_to='user-files/olimpiad-docs/', blank=True, null=True)
#     ielts = models.FileField(upload_to='user-files/language-certificates/ielts/', blank=True, null=True)
#     toefl = models.FileField(upload_to='user-files/language-certificates/toefl/', blank=True, null=True) #10
#     other_lang_cert = models.FileField(upload_to='user-files/language-certificates/other/', blank=True, null=True)
#     experience_doc = models.FileField(upload_to='user-files/experience-docs/', blank=True, null=True)
#     program_cert = models.FileField(upload_to='user-files/program-certificates/', blank=True, null=True)
#     sport_cert = models.FileField(upload_to='user-files/sport-certificates/', blank=True, null=True)
#     special_skills_doc = models.FileField(upload_to='user-files/special-skills-docs/', blank=True, null=True)
    
#     class Meta:
#         verbose_name = 'User Files'
#         verbose_name_plural = 'User Files'
    
#     def __str__(self) -> str:
#         return self.user.email