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


class GameDetail(generics.RetrieveAPIView):
    """
    Concrete view for retrieving a model instance.
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Game.objects.all()
    serializer_class = GameReadSerializer


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


class GameUpdate(generics.UpdateAPIView):
    """
    Concrete view for updating a model instance.
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Game.objects.all()
    serializer_class = GameWriteSerializer

    def perform_update(self, serializer):
        game_instance = serializer.save()
        date_values = self.request.data.get('dates')
        removed_dates = self.request.data.get('datesRemoved')

        # create any new dates in the request
        if date_values:
            for date in date_values:
                GameDateRelation.objects.get_or_create(
                    owner=self.request.user,
                    date=date,
                    game=game_instance,
                )

        # delete any dates that have been removed
        if removed_dates:
            for date in removed_dates:
                gdr = GameDateRelation.objects.get(
                    owner=self.request.user,
                    date=date,
                    game=game_instance,
                )
                gdr.delete()
