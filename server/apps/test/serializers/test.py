from rest_framework.serializers import ModelSerializer

from apps.test.models import Test


class TestSerializer(ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'
        read_only_fields = ('random_string', )