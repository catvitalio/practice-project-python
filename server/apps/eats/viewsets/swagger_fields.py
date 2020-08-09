from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

id_parameter = openapi.Parameter(
    'id', in_=openapi.IN_PATH,
    type=openapi.TYPE_STRING,
    description='Идентификатор'
)
token_parameter = openapi.Parameter(
    'Authorization', in_=openapi.IN_HEADER,
    type=openapi.TYPE_STRING,
    description='Токен для авторизации пользователя',
    pattern='Token *',
)

id_field = swagger_auto_schema(manual_parameters=[id_parameter])
token_field = swagger_auto_schema(manual_parameters=[token_parameter])
token_id_field = swagger_auto_schema(manual_parameters=[
    id_parameter,
    token_parameter,
])
