from rest_framework.viewsets import ModelViewSet

from apps.eats.models import Place
from apps.eats.serializers import PlaceSerializer


class PlaceViewSet(ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
