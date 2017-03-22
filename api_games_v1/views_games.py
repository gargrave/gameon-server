from rest_framework import generics, mixins, permissions
from rest_framework.response import Response

from .models import Game
from .serializers import GameSerializer


class GameList(generics.ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GameSerializer

    def get(self, request, *args, **kwargs):
        # if a 'search' query param is provided, filter by that value
        search_query = request.GET.get('search', '')

        if search_query == '':
            self.queryset = Game.objects\
                .filter(owner=self.request.user) \
                .exclude(archived=True)
        else:
            self.queryset = Game.objects \
                .filter(owner=self.request.user) \
                .filter(title__icontains=search_query)
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer
