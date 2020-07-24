from django.contrib.auth.models import User
from rest_framework.serializers import CurrentUserDefault
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import PrimaryKeyRelatedField

from apps.eats.models import Place


class PlaceSerializer(ModelSerializer):
    owner = PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=CurrentUserDefault()
    )

    class Meta:
        model = Place
        fields = '__all__'
