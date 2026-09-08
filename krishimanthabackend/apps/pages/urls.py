from rest_framework.routers import DefaultRouter
from .views import StaticPageViewSet

router = DefaultRouter()
router.register("", StaticPageViewSet, basename="static-page")
urlpatterns = router.urls
