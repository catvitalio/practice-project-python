from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from yandex_geocoder import Client

from apps.eats.models import Place


@receiver(pre_save, sender=Place)
def find_coordinates(sender, instance, **kwargs):
    client = Client(settings.GEO_API_KEY)
    coordinates = client.coordinates(instance.address)
    instance.latitude = coordinates[-1]
    instance.longitude = coordinates[0]
