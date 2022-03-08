from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Contributor, Project


class IsAuthorOrReadOnly(BasePermission):
    """
    Only allow author of a resource to perform update or delete operations.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        author = obj.author

        return user == author


class IsProjectManager(BasePermission):
    """
    Only allow the project manager to perform specific operations.
    """

    def has_permission(self, request, view):
        # Contributors are allowed to do that.
        if request.method in SAFE_METHODS:
            return True

        project_id = view.kwargs.get("project_id")
        project = Project.objects.get(pk=project_id)

        return project.author == request.user


class IsProjectContributor(BasePermission):
    """
    Only allow the project contributors to access to a project's ressources.
    """

    def has_permission(self, request, view):
        user = request.user
        project_id = view.kwargs.get("project_id")

        query_set = Contributor.objects.filter(
            user=user, project_id=project_id
        )

        return query_set.exists()
