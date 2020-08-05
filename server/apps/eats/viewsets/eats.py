from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from url_filter.integrations.drf import DjangoFilterBackend

from apps.eats.models import Place
from apps.eats.models import Ingredient
from apps.eats.models import Dish
from apps.eats.serializers import PlaceSerializer
from apps.eats.serializers import IngredientSerializer
from apps.eats.serializers import DishSerializer


class PlaceViewSet(ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name', 'owner', 'open_time', 'close_time', 'longitude', 'latitude']


class IngredientViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name', 'calories']


class DishViewSet(ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name', 'calories', 'place', 'cost', 'ingredients']
