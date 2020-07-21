from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from apps.test.models import Test


@receiver(pre_save, sender=Test)
def generate_random_string(sender, instance, **kwargs):
    instance.random_string = get_random_string(length=32)
