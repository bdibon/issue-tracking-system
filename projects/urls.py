from rest_framework.routers import SimpleRouter
from django.urls import path

from .views import (
    ProjectIssueListCreateView,
    ProjectIssueRetrieveUpdateDelete,
    ProjectViewSet,
    ProjectContributorsListView,
    ProjectContributorRetrieveDeleteView,
)

router = SimpleRouter()
router.register("projects", ProjectViewSet, basename="projects")

urlpatterns = [
    path(
        "projects/<int:pk>/users/",
        ProjectContributorsListView.as_view(),
        name="project_contributor_list",
    ),
    path(
        "projects/<int:project_id>/users/<int:contributor_id>/",
        ProjectContributorRetrieveDeleteView.as_view(),
        name="project_contributor_detail",
    ),
    path(
        "projects/<int:project_id>/issues/",
        ProjectIssueListCreateView.as_view(),
        name="project_issue_list",
    ),
    path(
        "projects/<int:project_id>/issues/<int:issue_id>/",
        ProjectIssueRetrieveUpdateDelete.as_view(),
        name="project_issue_detail",
    ),
]

urlpatterns += router.urls
