from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, mixins
from rest_framework.response import Response
from rest_framework import status, renderers

from .serializers import (
    ContributorReadSerializer,
    ContributorWriteSerializer,
    ProjectSerializer,
)
from .models import Project, Contributor
from .permissions import IsAuthorOrReadOnly
from .renderers import ProjectContributorListRenderer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    A ViewSet to perform CRUD operations on projects.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthorOrReadOnly]


class ProjectContributorsListView(generics.ListCreateAPIView):
    """
    List and add contributors to a specific project.
    """

    serializer_class = ContributorReadSerializer
    renderer_classes = [renderers.JSONRenderer, ProjectContributorListRenderer]
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        project_id = self.kwargs.get(self.lookup_field)
        return Contributor.objects.filter(
            project__id__iexact=project_id
        ).prefetch_related("user")

    def create(self, request, *args, **kwargs):
        user_id = request.data["user_id"]
        project_id = kwargs["pk"]
        serializer = ContributorWriteSerializer(
            data={"user": user_id, "project": project_id}
        )

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectContributorRetrieveDeleteView(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    Retrieve or destroy a project's contributor.
    """

    serializer_class = ContributorReadSerializer

    def get_object(self):
        return get_object_or_404(self.get_queryset())

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        contributor_id = self.kwargs.get("contributor_id")

        return Contributor.objects.filter(
            pk=contributor_id, project__id=project_id
        )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
