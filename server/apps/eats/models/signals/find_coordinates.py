from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from rest_framework.exceptions import APIException
from yandex_geocoder import Client
from yandex_geocoder.exceptions import InvalidKey
from yandex_geocoder.exceptions import NothingFound

from apps.eats.models import Place


@receiver(pre_save, sender=Place)
def find_coordinates(sender, instance, **kwargs):
    try:
        client = Client(settings.GEO_API_KEY)
        coordinates = client.coordinates(instance.address)
        instance.latitude = coordinates[-1]
        instance.longitude = coordinates[0]
    except NothingFound:
        raise APIException("Адрес заведения не найден")
    except InvalidKey:
        raise APIException("API-ключ Геокодера неверный")
