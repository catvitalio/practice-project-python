from django.db.models.signals import pre_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db.models import Avg

from apps.eats.models import Place
from apps.eats.models import Dish


@receiver(pre_save, sender=Dish)
@receiver(post_delete, sender=Dish)
def calculate_average_cost(sender, instance, **kwargs):
    place = Place.objects.get(id=instance.place.id)
    avg = Dish.objects.filter(
        place__id__exact=place.id).aggregate(Avg('cost'))
    if avg['cost__avg'] is not None:
        place.average_cost = avg['cost__avg']
    else:
        place.average_cost = 0
    place.save()
