from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ensayo, EnsayoGranulometria

@receiver(post_save, sender=Ensayo)
def crear_modelo_especifico(sender, instance, created, **kwargs):
    if created:
        if instance.tipo.codigo == "GRANULOMETRIA":
            EnsayoGranulometria.objects.create(ensayo=instance)