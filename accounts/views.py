from rest_framework import viewsets
from django.contrib.auth import get_user_model

from .serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List or retrieve the user resource.
    """

    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
