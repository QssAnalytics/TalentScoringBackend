# class FileCategory(models.Model):
#     name = models.CharField(max_length=50)
#     file_count = models.PositiveIntegerField(default=0, editable=False)  # Field to store the file count
#     allows_multiple_files = models.BooleanField(default=False)
    
#     def __str__(self):
#         return self.name


# class UserFile(models.Model):
#     user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
#     category = models.ForeignKey(FileCategory, on_delete=models.CASCADE)
#     file = models.FileField(upload_to=user_file_upload_path, null=True, blank=True)
    
#     class Meta:
#         verbose_name = 'User File'
#         verbose_name_plural = 'User Files'
    
#     def __str__(self):
#         return f"{self.user.email} - {self.category}"
    
#     def save(self, *args, **kwargs):
#         # Increment the file count for the category when a new UserFile is created
#         if not self.pk: 
#             self.category.file_count += 1
#             self.category.save()
#         super().save(*args, **kwargs)
    
#     def delete(self, *args, **kwargs):
#         # Decrement the file count for the category when a UserFile is deleted
#         self.category.file_count -= 1
#         self.category.save()
#         super().delete(*args, **kwargs)

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