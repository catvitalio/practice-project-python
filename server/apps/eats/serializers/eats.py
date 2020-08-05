from django.contrib.auth.models import User
from rest_framework.serializers import CurrentUserDefault
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import PrimaryKeyRelatedField

from apps.eats.models import Place
from apps.eats.models import Ingredient
from apps.eats.models import Dish


class PlaceSerializer(ModelSerializer):
    owner = PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=CurrentUserDefault()
    )

    class Meta:
        model = Place
        fields = '__all__'


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class DishSerializer(ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'
