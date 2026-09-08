from rest_framework.routers import DefaultRouter
from .views import EPaperIssueViewSet

router = DefaultRouter()
router.register("", EPaperIssueViewSet, basename="epaper")
urlpatterns = router.urls
