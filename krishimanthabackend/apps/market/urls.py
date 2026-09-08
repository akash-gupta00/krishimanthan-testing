from rest_framework.routers import DefaultRouter
from .views import MarketPriceViewSet

router = DefaultRouter()
router.register("", MarketPriceViewSet, basename="market-price")
urlpatterns = router.urls
