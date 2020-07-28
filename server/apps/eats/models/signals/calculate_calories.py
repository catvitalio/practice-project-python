from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.models import Sum

from apps.eats.models import Dish
from apps.eats.models import Ingredient


@receiver(m2m_changed, sender=Dish.ingredients.through)
def calculate_calories(sender, instance, **kwargs):
    calories_sum = Ingredient.objects.filter(
        dish__id__exact=instance.id).aggregate(Sum('calories'))
    instance.calories = calories_sum['calories__sum']
    instance.save()
