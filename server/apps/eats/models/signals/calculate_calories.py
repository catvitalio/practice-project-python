from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from apps.eats.models import Dish


@receiver(m2m_changed, sender=Dish.ingredients.through)
def calculate_calories(sender, instance, **kwargs):
    instance.calories = Dish.objects.with_sum_calories(instance.id)
    instance.save()
