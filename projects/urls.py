from rest_framework.routers import SimpleRouter
from django.urls import path

from .views import (
    CommentListCreateView,
    CommentRetrieveUpdateDestroyView,
    IssueListCreateView,
    IssueRetrieveUpdateDelete,
    ProjectViewSet,
    ContributorsListCreateView,
    ContributorRetrieveDeleteView,
)

router = SimpleRouter()
router.register("projects", ProjectViewSet, basename="projects")

urlpatterns = [
    path(
        "projects/<int:project_id>/users/",
        ContributorsListCreateView.as_view(),
        name="project_contributor_list",
    ),
    path(
        "projects/<int:project_id>/users/<int:contributor_id>/",
        ContributorRetrieveDeleteView.as_view(),
        name="project_contributor_detail",
    ),
    path(
        "projects/<int:project_id>/issues/",
        IssueListCreateView.as_view(),
        name="project_issue_list",
    ),
    path(
        "projects/<int:project_id>/issues/<int:issue_id>/",
        IssueRetrieveUpdateDelete.as_view(),
        name="project_issue_detail",
    ),
    path(
        "projects/<int:project_id>/issues/<int:issue_id>/comments/",
        CommentListCreateView.as_view(),
        name="issue_comment_list",
    ),
    path(
        "projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>/",  # noqa E501
        CommentRetrieveUpdateDestroyView.as_view(),
        name="issue_comment_detail",
    ),
]

urlpatterns += router.urls
