from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from apps.users.serializers import UserSerializer


class UserViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
