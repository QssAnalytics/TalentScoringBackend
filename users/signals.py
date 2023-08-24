from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CertificateModel, UniqueRandom

@receiver(post_save, sender=CertificateModel)
def create_unique_key(sender, instance, created, **kwargs):
    if created:
      if instance.cert_unique_key is not None:
        unq_key = UniqueRandom.objects.create(unique_value=instance.cert_unique_key)
        unq_key.save()