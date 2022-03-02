from rest_framework.routers import SimpleRouter

from .views import ProjectViewSet

router = SimpleRouter()
router.register("projects", ProjectViewSet, basename="projects")

urlpatterns = router.urls
