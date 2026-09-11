"""
Django settings for Krishi Manthan backend.
Config is driven entirely by environment variables (see .env.example) —
never hardcode secrets/passwords in code.
"""
import os
from pathlib import Path
from datetime import timedelta
import environ
import cloudinary

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, True),
)
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("DJANGO_SECRET_KEY", default="dev-only-insecure-secret-key-change-me")
DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

# ------------------------------------------------------------------
# Applications
# ------------------------------------------------------------------
DJANGO_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "cloudinary_storage",
    "django.contrib.staticfiles",
    "cloudinary",
    "apps",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
    "tinymce",
]

LOCAL_APPS = [
    "apps.core",
    "apps.accounts",
    "apps.sitesettings",
    "apps.departments",
    "apps.news",
    "apps.schemes",
    "apps.events",
    "apps.resources",
    "apps.ads",
    "apps.announcements",
    "apps.market",
    "apps.weather",
    "apps.contact",
    "apps.subscribers",
    "apps.faqs",
    "apps.testimonials",
    "apps.about",
    "apps.epaper",
    "apps.llmintegration",
    "apps.searchapi",
    "apps.pages",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ------------------------------------------------------------------
# Database — PostgreSQL (Persistent connection + Health check)
# ------------------------------------------------------------------
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="postgres://krishimanthan:krishimanthan_dev_pass@localhost:5432/krishimanthan_db",
    )
}

DATABASES["default"]["CONN_MAX_AGE"] = 600
DATABASES["default"]["CONN_HEALTH_CHECKS"] = True

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTH_USER_MODEL = "accounts.User"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------
# Static & Media Storage Configuration
# ------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Standard storage ignores missing map/css files during build
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ------------------------------------------------------------------
# Cloudinary Storage Configuration (via CLOUDINARY_URL)
# ------------------------------------------------------------------
CLOUDINARY_URL_ENV = env(
    "CLOUDINARY_URL",
    default="cloudinary://915116215253549:dyjdVS__dwgQOG7AQv58JI6PD9I@afemxggo",
)

# Set environment variable explicitly for SDK auto-detection
os.environ["CLOUDINARY_URL"] = CLOUDINARY_URL_ENV

cloudinary.config(
    cloudinary_url=CLOUDINARY_URL_ENV,
    secure=True,
)

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------------------------------------------
# DRF
# ------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 12,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "120/minute",
        "user": "300/minute",
    },
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=8),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Krishi Manthan API",
    "DESCRIPTION": "Backend API powering the Krishi Manthan agriculture portal.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": "/api/v1/",
}

# ------------------------------------------------------------------
# CORS, CSRF & Iframe Security
# ------------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=True)
CORS_ALLOW_CREDENTIALS = True

X_FRAME_OPTIONS = "ALLOWALL"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

CSRF_TRUSTED_ORIGINS = [
    "https://krishimanthan-testing.onrender.com",
    "https://krishimanthan.in",
    "https://www.krishimanthan.in",
    "http://localhost:5173",
    "http://localhost:3000",
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ------------------------------------------------------------------
# LLM integration
# ------------------------------------------------------------------
LLM_PROVIDER = env("LLM_PROVIDER", default="none")
LLM_API_KEY = env("LLM_API_KEY", default="")
LLM_MODEL = env("LLM_MODEL", default="claude-sonnet-4-6")

# ------------------------------------------------------------------
# Weather (OpenWeatherMap)
# ------------------------------------------------------------------
WEATHER_API_KEY = env("WEATHER_API_KEY", default="")
WEATHER_API_PROVIDER = env("WEATHER_API_PROVIDER", default="openweathermap")

# ------------------------------------------------------------------
# Email
# ------------------------------------------------------------------
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="no-reply@krishimanthan.in")
CONTACT_NOTIFY_EMAIL = env("CONTACT_NOTIFY_EMAIL", default="info@krishimanthan.in")

# ------------------------------------------------------------------
# Upload hardening
# ------------------------------------------------------------------
DATA_UPLOAD_MAX_MEMORY_SIZE = 25 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 25 * 1024 * 1024
FILE_UPLOAD_PERMISSIONS = 0o644

# ------------------------------------------------------------------
# TinyMCE
# ------------------------------------------------------------------
TINYMCE_DEFAULT_CONFIG = {
    "height": 320,
    "menubar": "edit view insert format tools",
    "plugins": "advlist autolink lists link charmap preview searchreplace visualblocks code fullscreen wordcount",
    "toolbar": "undo redo | formatselect | bold italic underline | bullist numlist | link | removeformat | code fullscreen",
    "branding": False,
    "resize": True,
}

# ------------------------------------------------------------------
# Jazzmin
# ------------------------------------------------------------------
JAZZMIN_SETTINGS = {
    "site_title": "Krishi Manthan Admin",
    "site_header": "Krishi Manthan",
    "site_brand": "Krishi Manthan",
    "welcome_sign": "Krishi Manthan content management",
    "copyright": "Krishi Manthan",
    "search_model": ["news.NewsItem", "schemes.Scheme", "events.Event"],
    "show_sidebar": True,
    "navigation_expanded": False,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": [
        "sitesettings", "about", "departments", "news", "schemes", "events",
        "resources", "ads", "announcements", "market", "weather",
        "epaper", "faqs", "testimonials", "contact", "subscribers", "accounts", "auth",
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.Group": "fas fa-users",
        "accounts.User": "fas fa-user-shield",
        "sitesettings.SiteSettings": "fas fa-cog",
        "about.AboutContent": "fas fa-info-circle",
        "about.AboutHighlight": "fas fa-star",
        "departments.Department": "fas fa-building",
        "news.NewsItem": "fas fa-newspaper",
        "news.NewsCategory": "fas fa-tags",
        "schemes.Scheme": "fas fa-landmark",
        "events.Event": "fas fa-calendar-alt",
        "resources.Resource": "fas fa-file-download",
        "ads.Advertisement": "fas fa-ad",
        "ads.AdSlot": "fas fa-th-large",
        "announcements.Announcement": "fas fa-bullhorn",
        "market.MarketPrice": "fas fa-chart-line",
        "weather.WeatherCity": "fas fa-cloud-sun",
        "epaper.EPaperIssue": "fas fa-book-open",
        "faqs.FAQ": "fas fa-question-circle",
        "testimonials.Testimonial": "fas fa-quote-right",
        "contact.ContactMessage": "fas fa-envelope",
        "subscribers.Subscriber": "fas fa-user-plus",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": None,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-success",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "flatly",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-success",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}