from django.contrib import admin
from .models import UserAccount, ReportModel,CertificateModel, UniqueRandom, UserFile, FileCategory
# Register your models here.
admin.site.register(UserAccount) 
admin.site.register(ReportModel) 
admin.site.register(CertificateModel)
admin.site.register(UniqueRandom)


admin.site.register(UserFile)
admin.site.register(FileCategory)
