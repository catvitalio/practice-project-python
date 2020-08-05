from django.db.models.signals import pre_save
from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.eats.models import Place
from apps.eats.models import Dish


@receiver(pre_save, sender=Dish)
@receiver(post_delete, sender=Dish)
def calculate_average_cost(sender, instance, **kwargs):
    place = Place.objects.get(id=instance.place.id)
    place.average_cost = Place.objects.with_avg_cost(instance.place.id)
    place.save()
