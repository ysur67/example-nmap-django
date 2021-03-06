from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)


schema_view = get_schema_view(
   openapi.Info(
      title="Tasks API",
      default_version='v1',
      description="Тестовое задание",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('', RedirectView.as_view(url='/swagger/')),
   path("swagger/", schema_view.with_ui("swagger"), name="schema-swagger-ui"),
   path('admin/', admin.site.urls),
   path('api/v1/', include(("tasks.urls", "tasks"))),
   path('api/v1/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
   path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
