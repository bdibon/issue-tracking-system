from rest_framework import viewsets

from .serializers import ProjectSerializer
from .models import Project


class ProjectViewSet(viewsets.ModelViewSet):
    """
    A ViewSet to perform CRUD operations on projects.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
