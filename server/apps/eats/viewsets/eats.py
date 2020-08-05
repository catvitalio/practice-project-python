from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from url_filter.integrations.drf import DjangoFilterBackend

from apps.eats.models import Place, Ingredient, Dish
from apps.eats.serializers import PlaceSerializer
from apps.eats.serializers import IngredientSerializer
from apps.eats.serializers import DishSerializer
from apps.main.permissions import PlacePermission, DishPermission


class PlaceViewSet(ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name', 'owner', 'open_time', 'close_time', 'longitude', 'latitude']
    permission_classes = [PlacePermission]


class IngredientViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name', 'calories']
    permission_classes = [IsAuthenticatedOrReadOnly]


class DishViewSet(ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name', 'calories', 'place', 'cost', 'ingredients']
    permission_classes = [DishPermission]
