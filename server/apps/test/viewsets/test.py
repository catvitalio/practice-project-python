from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from apps.test.models import Test
from apps.test.serializers import TestSerializer


class TestViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet
):
    serializer_class = TestSerializer
    queryset = Test.objects.all()
