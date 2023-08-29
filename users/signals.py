from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CertificateModel, UniqueRandom, ReportModel

# @receiver(post_save, sender=CertificateModel)
# def create_unique_key_certificate(sender, instance, created, **kwargs):
#     if created:
#       if instance.cert_unique_key is not None:
#         unq_key = UniqueRandom.objects.create(unique_value=instance.cert_unique_key) #TODO: add user
#         unq_key.save()

# @receiver(post_save, sender=ReportModel)
# def create_unique_key_report(sender, instance, created, **kwargs):
#     if created:
#       if instance.cert_unique_key is not None:
#         unq_key = UniqueRandom.objects.create(unique_value=instance.cert_unique_key) #TODO: add user
#         unq_key.save()