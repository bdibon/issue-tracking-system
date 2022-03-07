from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from projects.permissions import IsAuthorOrReadOnly

from .serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List or retrieve the user resource.
    """

    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthorOrReadOnly]
