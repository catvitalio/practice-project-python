from rest_framework import routers

from apps.test.viewsets import TestViewSet
from apps.users.viewsets import UserViewSet
from apps.eats.viewsets import PlaceViewSet
from apps.eats.viewsets import IngredientViewSet
from apps.eats.viewsets import DishViewSet


router = routers.DefaultRouter()
router.register('test', TestViewSet, basename='test')
router.register('users', UserViewSet, basename='users')
router.register('places', PlaceViewSet, basename='places')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('dishes', DishViewSet, basename='dishes')
