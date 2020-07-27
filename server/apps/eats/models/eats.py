from django.contrib.auth.models import User
from django.db import models


class Place(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название заведения',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        blank=True,
        null=True,
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
    open = models.TimeField(
        verbose_name='Время открытия',
        blank=True,
        null=True,
    )
    close = models.TimeField(
        verbose_name='Время закрытия',
        blank=True,
        null=True,
    )
    latitude = models.FloatField(
        verbose_name='Координаты (широта)',
        blank=True,
        null=True,
    )
    longitude = models.FloatField(
        verbose_name='Координаты (долгота)',
        blank=True,
        null=True,
    )
    average_cost = models.FloatField(
        verbose_name='Средняя стоимость блюд',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Заведение'
        verbose_name_plural = 'Заведение'
