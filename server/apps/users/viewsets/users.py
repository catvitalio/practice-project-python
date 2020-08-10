from django.utils.decorators import method_decorator
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from apps.users.serializers import UserSerializer
from .swagger_fields import without_password


@method_decorator(name='create', decorator=without_password)
class UserViewSet(CreateModelMixin, GenericViewSet):
    """
    create: Создание нового пользователя
    """
    serializer_class = UserSerializer
