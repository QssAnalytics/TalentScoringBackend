import os
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.core.files.storage import default_storage
from django.dispatch import receiver
from django.utils.text import slugify


class Answer(models.Model):
    questionIdd = models.ForeignKey(
        "app.Question", on_delete=models.CASCADE, related_name='answers')
    answer_title = models.CharField(max_length=100, null=True, blank=True)
    answer_weight = models.DecimalField(max_digits=9,
                                        decimal_places=4,
                                        null=True,
                                        blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    answer_dependens_on = models.ForeignKey('self', on_delete=models.PROTECT,
                                             null=True,
                                               blank=True)
    stage_fit = models.OneToOneField('app.Stage', on_delete=models.PROTECT, null=True,blank=True)
    
    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


    def get_stage_slug(self):
        if self.stage_fit is not None:
            return self.stage_fit.slug
        return None
    def __str__(self):
        if self.questionIdd_id:
            return "answer={}; question={}".format(self.answer_title, self.questionIdd.question_title)
        else:
            return "answer={}; question=None".format(self.answer_title)
    
class Question(models.Model):

    question_title = models.CharField(verbose_name='question', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stage=models.ForeignKey('app.Stage', related_name = 'questions', on_delete=models.CASCADE)
    question_dependens_on_answer = models.ForeignKey('app.Answer', related_name = 'questions', blank=True,null=True, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=50, blank=True, null=True)
    question_dependens_on_question = models.ForeignKey('self', blank=True, null=True, related_name='question_depend', on_delete=models.CASCADE)
    question_index = models.IntegerField(blank=True, null=True)
    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
    
        ordering = ['stage__stage_name', 'question_index']

    def __str__(self):
        
        return self.question_title
    
class Stage(models.Model):
    stage_name = models.CharField(max_length = 150)
    parent=models.ForeignKey('self', blank=True, null=True, related_name='stage_children', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, blank=True)
    stage_index = models.IntegerField(blank=True, null=True)
    #stage_dependens_on = models.ForeignKey('app.Answer', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.stage_name
    
    class Meta:
        ordering = ['stage_index']
    

    def save(self, *args, **kwargs):
        if self.stage_name:
            self.slug=slugify(self.stage_name.replace('ı','i').replace('ə','e').replace('ö','o').replace('ü','u').replace('ç','c')\
                              .replace("I", "I").replace('Ə','E').replace('Ö','O').replace('Ü','U').replace('Ç','C'))
            
        return super().save(*args, **kwargs)
            


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
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

#first_name, last_name, email, password,password2, birth_date, gender, native_language, country

GENDER_CHOICES = (
    ("Female", "Female"),
    ("Male", "Male"),

)

class UserAccount(AbstractBaseUser):
    # username = models.CharField(max_length = 150, unique=True)
    first_name = models.CharField(max_length = 150, null=True, blank = True)
    last_name = models.CharField(max_length = 150, null=True, blank = True)
    email = models.EmailField(unique=True, blank=True, null=True)
    birth_date = models.DateField( blank=True, null=True)
    gender = models.CharField(max_length=10, choices = GENDER_CHOICES, blank=True, null=True)
    native_language = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    # age = models.IntegerField(blank=True, null=True)
    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    user_info = models.JSONField(blank=True, null=True)
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


def file_directory(instance, filname):
    return "report{0}{1}".format(instance.id, filname)


class UserProfile(models.Model):
    user = models.ForeignKey(
        'app.UserAccount', models.CASCADE
    )
    report_file = models.FileField(upload_to='images/') 

    def __str__(self) -> str:
        return self.user.email 
    
    def delete(self,*args,**kwargs):
        default_storage.delete(self.report_file.name)
        super().delete(*args, **kwargs)

# @receiver(models.signals.post_delete, sender=UserProfile)
# def auto_delete_file_on_delete(sender, instance, **kwargs):
#     """
#     Deletes file from filesystem
#     when corresponding `MediaFile` object is deleted.
#     """
#     if instance.file:
#         if os.path.isfile(instance.file.path):
#             os.remove(instance.file.path)

# @receiver(models.signals.pre_save, sender=UserProfile)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#     """
#     Deletes old file from filesystem
#     when corresponding `MediaFile` object is updated
#     with new file.
#     """
#     if not instance.pk:
#         return False

#     try:
#         old_file = UserProfile.objects.get(pk=instance.pk).file
#     except UserProfile.DoesNotExist:
#         return False

#     new_file = instance.file
#     if not old_file == new_file:
#         if os.path.isfile(old_file.path):
#             os.remove(old_file.path)