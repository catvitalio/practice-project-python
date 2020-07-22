from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.users.serializers import UserSerializer


class UserViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = UserSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {}
        account = serializer.save()
        headers = self.get_success_headers(serializer.data)
        token = Token.objects.get(user=account).key
        data['token'] = token
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
