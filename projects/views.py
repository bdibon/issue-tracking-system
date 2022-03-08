from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, mixins, status, renderers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    ContributorRetrieveSerializer,
    ContributorCreateSerializer,
    IssueSerializer,
    ProjectCreateSerializer,
    ProjectSerializer,
)
from .models import Issue, Project, Contributor
from .permissions import (
    IsAuthorOrReadOnly,
    IsProjectContributor,
    IsProjectManager,
)
from .renderers import ProjectContributorListRenderer, ProjectCreateRenderer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    A ViewSet to perform CRUD operations on projects.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    renderer_classes = [renderers.JSONRenderer, ProjectCreateRenderer]

    def create(self, request, *args, **kwargs):
        project_author = request.user
        serializer = ProjectCreateSerializer(
            data={
                "author": project_author.id,
                "title": request.data["title"],
                "description": request.data["description"],
                "type": request.data["type"],
            }
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

    # This is not consistent with REST conventions, however as I have been playing with
    # custom renderers I'll allow myself this fantasy.
    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)


class ProjectContributorsListView(generics.ListCreateAPIView):
    """
    List and add contributors to a specific project.
    """

    serializer_class = ContributorRetrieveSerializer
    renderer_classes = [renderers.JSONRenderer, ProjectContributorListRenderer]
    permission_classes = [IsAuthenticated, IsProjectManager]

    def get_queryset(self):
        project_id = self.kwargs.get(self.lookup_field)
        return Contributor.objects.filter(
            project__id__iexact=project_id
        ).prefetch_related("user")

    def create(self, request, *args, **kwargs):
        user_id = request.data["user_id"]
        project_id = kwargs["pk"]
        serializer = ContributorCreateSerializer(
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

    serializer_class = ContributorRetrieveSerializer
    permission_classes = [IsAuthenticated, IsProjectManager]

    def get_object(self):
        obj = get_object_or_404(self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj

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


class ProjectIssueListCreateView(generics.ListCreateAPIView):
    """
    List and add issues to a project.
    """

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor]
    lookup_field = "project_id"

    def get_queryset(self):
        project_id = self.kwargs.get(self.lookup_field)
        return Issue.objects.filter(project__id=project_id)

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs.get(self.lookup_field)
        data = {
            **request.data,
            "project_id": project_id,
            "author_id": request.user.id,
        }
        serializer = IssueSerializer(data=data)

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectIssueRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IssueSerializer
    permission_classes = [
        IsAuthenticated,
        IsProjectContributor,
        IsAuthorOrReadOnly,
    ]

    def get_object(self):
        project_id = self.kwargs.get("project_id")
        issue_id = self.kwargs.get("issue_id")
        query_set = Issue.objects.filter(pk=issue_id, project_id=project_id)
        issue = get_object_or_404(query_set)
        return issue
