from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.api.routers import router


schema_view = get_schema_view(
    openapi.Info(
        title="Places API",
        default_version='v1',
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api_doc/', schema_view.with_ui('swagger', cache_timeout=0)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    import debug_toolbar

    urlpatterns += [
          path('__debug__/', include(debug_toolbar.urls)),
    ]
