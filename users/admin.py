from django.contrib import admin
from .models import UserAccount, ReportModel,CertificateModel
# Register your models here.
admin.site.register(UserAccount) 
admin.site.register(ReportModel) 
admin.site.register(CertificateModel)