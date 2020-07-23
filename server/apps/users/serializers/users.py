from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField


class UserSerializer(ModelSerializer):
    token = SerializerMethodField()

    def get_token(self, instance):
        token = Token.objects.get(user=instance).key
        return token

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token', )
        extra_kwargs = {'password': {'write_only': True}}
