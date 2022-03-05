from rest_framework.routers import SimpleRouter
from django.urls import path

from .views import ProjectViewSet, ProjectContributorsListView

router = SimpleRouter()
router.register("projects", ProjectViewSet, basename="projects")

urlpatterns = [
    path(
        "projects/<int:pk>/users/",
        ProjectContributorsListView.as_view(),
        name="project_contributors",
    )
]
urlpatterns += router.urls
