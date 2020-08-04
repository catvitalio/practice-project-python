from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg, Sum


class PlaceManager(models.Manager):
    def with_avg_cost(self, place_id):
        avg_cost = Dish.objects.filter(
            place__id__exact=place_id).aggregate(Avg('cost'))
        return avg_cost['cost__avg']


class Place(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название заведения',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
    )
    photo = models.ImageField(
        upload_to='places/',
        verbose_name='Фотография заведения',
        blank=True,
    )
    address = models.CharField(
        max_length=255,
        verbose_name='Адрес заведения',
    )
    open_time = models.TimeField(
        verbose_name='Время открытия',
        blank=True,
        null=True,
    )
    close_time = models.TimeField(
        verbose_name='Время закрытия',
        blank=True,
        null=True,
    )
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        verbose_name='Координаты (широта)',
        blank=True,
        null=True,
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        verbose_name='Координаты (долгота)',
        blank=True,
        null=True,
    )
    average_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Средняя стоимость блюд',
        blank=True,
        null=True,
    )
    objects = PlaceManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Заведение'
        verbose_name_plural = 'Заведения'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название ингредиента',
    )
    calories = models.PositiveSmallIntegerField(
        verbose_name='Калорийность ингредиента (ккал)',
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class DishManager(models.Manager):
    def with_sum_calories(self, dish_id):
        sum_calories = Ingredient.objects.filter(
            dish__id__exact=dish_id).aggregate(Sum('calories'))
        return sum_calories['calories__sum']


class Dish(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название блюда',
    )
    photo = models.ImageField(
        upload_to='dishes/',
        verbose_name='Фотография блюда',
        blank=True,
    )
    calories = models.PositiveSmallIntegerField(
        verbose_name='Суммарная калорийность (ккал)',
        blank=True,
        null=True,
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Стоимость блюда',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        verbose_name='Заведение блюда'
    )
    objects = DishManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
