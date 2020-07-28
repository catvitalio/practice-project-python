from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin

from apps.eats.models import Place
from apps.eats.models import Ingredient
from apps.eats.models import Dish
from apps.eats.serializers import PlaceSerializer
from apps.eats.serializers import IngredientSerializer
from apps.eats.serializers import DishSerializer


class PlaceViewSet(ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class IngredientViewSet(ListModelMixin,
                        RetrieveModelMixin,
                        GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class DishViewSet(ModelViewSet):
    serializer_class = DishSerializer

    def get_queryset(self):
        queryset = Dish.objects.all()
        place = self.request.query_params.get('place', None)
        if place is not None:
            queryset = queryset.filter(place_id=place)
        return queryset
