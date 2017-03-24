from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import PlatformModel
from .serializers import PlatformSerializer


class PlatformList(generics.ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PlatformSerializer

    def get_queryset(self):
        return PlatformModel.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
