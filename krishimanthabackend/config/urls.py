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

if settings.DEBUG:
    # Serve MEDIA_URL ourselves (instead of the default static() helper) so
    # we can exempt it from Django's default X-Frame-Options: DENY header.
    # Without this, the e-paper PDF (and any other media embedded in an
    # <iframe>, e.g. from the :8080 frontend) is silently blocked by the
    # browser even though the file itself loads fine — it just renders as
    # a blank/grey box. Media in production should be served by
    # nginx/S3/CDN, which won't add this header at all.
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            xframe_options_exempt(static_serve),
            {"document_root": settings.MEDIA_ROOT},
        ),
    ]
