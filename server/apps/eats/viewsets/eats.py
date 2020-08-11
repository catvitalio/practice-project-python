from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from url_filter.integrations.drf import DjangoFilterBackend

from apps.eats.models import Place, Ingredient, Dish
from apps.eats.serializers import PlaceSerializer
from apps.eats.serializers import IngredientSerializer
from apps.eats.serializers import DishSerializer
from apps.main.permissions import PlacePermission, DishPermission
from .swagger_fields import id_field, token_field, token_id_field


@method_decorator(name='retrieve', decorator=id_field)
@method_decorator(name='create', decorator=token_field)
@method_decorator(name='update', decorator=token_id_field)
@method_decorator(name='partial_update', decorator=token_id_field)
@method_decorator(name='destroy', decorator=token_id_field)
class PlaceViewSet(ModelViewSet):
    """
    list: Возврат списка всех заведений
    retrieve: Возврат заведения по id
    create: Создание нового заведения для авторизованного пользователя
    update: Обновление заведения по всем полям
    partial_update: Обновление заведения по заполненным полям
    destroy: Удаление заведения
    """
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name', 'owner', 'open_time', 'close_time', 'longitude', 'latitude']
    permission_classes = [PlacePermission]


@method_decorator(name='retrieve', decorator=id_field)
@method_decorator(name='create', decorator=token_field)
class IngredientViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    """
    list: Возврат списка всех ингредиентов
    retrieve: Возврат ингредиента по id
    create: Создание нового ингредиента
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name', 'calories']
    permission_classes = [IsAuthenticatedOrReadOnly]


@method_decorator(name='retrieve', decorator=id_field)
@method_decorator(name='create', decorator=token_field)
@method_decorator(name='update', decorator=token_id_field)
@method_decorator(name='partial_update', decorator=token_id_field)
@method_decorator(name='destroy', decorator=token_id_field)
class DishViewSet(ModelViewSet):
    """
    list: Возврат списка всех блюд
    retrieve: Возврат блюда по id
    create: Создание нового блюда для заведения
    update: Обновление блюда по всем полям
    partial_update: Обновление блюда по заполненным полям
    destroy: Удаление блюда
    """
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name', 'calories', 'place', 'cost', 'ingredients']
    permission_classes = [DishPermission]
