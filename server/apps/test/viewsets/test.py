from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from apps.test.models import Test
from apps.test.serializers import TestSerializer

decorator = swagger_auto_schema(
    auto_schema=None
)


@method_decorator(name='create', decorator=decorator)
@method_decorator(name='list', decorator=decorator)
@method_decorator(name='retrieve', decorator=decorator)
class TestViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet
):
    serializer_class = TestSerializer
    queryset = Test.objects.all()
