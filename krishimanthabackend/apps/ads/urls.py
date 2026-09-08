from rest_framework.routers import DefaultRouter
from .views import ActiveAdViewSet, AdSubmissionViewSet, AdSlotViewSet

router = DefaultRouter()
router.register("submit", AdSubmissionViewSet, basename="ad-submit")
router.register("slots", AdSlotViewSet, basename="ad-slot")
router.register("", ActiveAdViewSet, basename="ad")
urlpatterns = router.urls
