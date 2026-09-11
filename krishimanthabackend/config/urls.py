from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve as static_serve
from django.views.decorators.clickjacking import xframe_options_exempt
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

admin.site.site_header = "Krishi Manthan Admin"
admin.site.site_title = "Krishi Manthan Admin"
admin.site.index_title = "Content Management"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("api/v1/", include("config.api_urls")),

    # OpenAPI / Swagger documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# Media serving enabled unconditionally with iframe support
urlpatterns += [
    re_path(
        r"^media/(?P<path>.*)$",
        xframe_options_exempt(static_serve),
        {"document_root": settings.MEDIA_ROOT},
    ),
]