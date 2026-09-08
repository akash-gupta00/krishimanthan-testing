from django.urls import path, include
from apps.weather.views import CurrentWeatherView
from apps.about.views import AboutContentView
from apps.sitesettings.views import SiteSettingsView

urlpatterns = [
    path("auth/", include("apps.accounts.urls")),
    path("departments/", include("apps.departments.urls")),
    path("news/", include("apps.news.urls")),
    path("schemes/", include("apps.schemes.urls")),
    path("events/", include("apps.events.urls")),
    path("resources/", include("apps.resources.urls")),
    path("ads/", include("apps.ads.urls")),
    path("announcements/", include("apps.announcements.urls")),
    path("market-prices/", include("apps.market.urls")),
    path("weather/current/", CurrentWeatherView.as_view(), name="weather-current"),
    path("contact/", include("apps.contact.urls")),
    path("subscribers/", include("apps.subscribers.urls")),
    path("faqs/", include("apps.faqs.urls")),
    path("testimonials/", include("apps.testimonials.urls")),
    path("about/", AboutContentView.as_view(), name="about-content"),
    path("epaper/", include("apps.epaper.urls")),
    path("site-settings/", SiteSettingsView.as_view(), name="site-settings"),
    path("search/", include("apps.searchapi.urls")),
    path("llm/", include("apps.llmintegration.urls")),
    path("pages/", include("apps.pages.urls")),
]
