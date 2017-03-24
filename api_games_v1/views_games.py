"""
Views for the 'games' API endpoints.
"""
from rest_framework import generics, permissions

from .models import Game, GameDateRelation
from .serializers import GameReadSerializer, GameWriteSerializer


class GameList(generics.ListAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GameReadSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = Game.objects.filter(owner=self.request.user)
        return self.list(request, *args, **kwargs)


class GameCreate(generics.CreateAPIView):
    """
    Concrete view for creating a model instance.

    Adding a custom perform_create implementation to add GameDateRelations
    for any necessary dates provided with this request.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GameWriteSerializer

    def perform_create(self, serializer):
        game_instance = serializer.save(owner=self.request.user)
        date_values = self.request.data.get('dates')
        for date in date_values:
            GameDateRelation.objects.get_or_create(
                owner=self.request.user,
                date=date,
                game=game_instance,
            )


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Game.objects.all()
    serializer_class = GameReadSerializer
