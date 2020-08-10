from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

from apps.users.serializers import UserSerializer


class PostUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'token')


without_password = swagger_auto_schema(
    responses={status.HTTP_201_CREATED: openapi.Response(
        'Возврат id, username, token без пароля', PostUserSerializer
    )}
)
