from django.contrib import admin

from .models import Place
from .models import Ingredient
from .models import Dish


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    pass
