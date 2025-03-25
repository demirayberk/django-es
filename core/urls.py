from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi, views

# Schema view for Swagger
schema_view = views.get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="API documentation for Your Project",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        public=True,
    ),
    public=True,
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
