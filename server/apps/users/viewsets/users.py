from django.utils.decorators import method_decorator
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from apps.users.serializers import UserSerializer
from .swagger_fields import without_password, id_username_password


@method_decorator(name='create', decorator=without_password)
class UserViewSet(CreateModelMixin, GenericViewSet):
    """
    create: Создание нового пользователя
    """
    serializer_class = UserSerializer


@method_decorator(name='create', decorator=id_username_password)
class AuthViewSet(ViewSet):
    """
    create: Авторизация пользователя с возвратом токена
    """
    serializer_class = AuthTokenSerializer

    def create(self, request):
        return ObtainAuthToken().post(self.request)
