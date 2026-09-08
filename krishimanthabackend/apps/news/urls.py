from rest_framework.routers import DefaultRouter
from .views import NewsItemViewSet, NewsCategoryViewSet

router = DefaultRouter()
router.register("categories", NewsCategoryViewSet, basename="news-category")
router.register("", NewsItemViewSet, basename="news")
urlpatterns = router.urls
