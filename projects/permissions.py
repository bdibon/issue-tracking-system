from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Project


class IsAuthorOrReadOnly(BasePermission):
    """
    Only allow author of a resource to perform update or delete operations.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        # Determine if the current user is the owner of the resources.
        if view.__class__.__name__ == "ProjectContributorsListView":
            project_id = view.kwargs.get(view.lookup_field)
            project = Project.objects.get(pk=project_id)

            if project.author == request.user:
                return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        owner = obj.author

        return user == owner
