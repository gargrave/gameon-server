"""
Views for the 'games' API endpoints.
"""
from rest_framework import generics, permissions

from .models import Game, GameDateRelation, PlatformModel
from .serializers import GameReadSerializer, GameWriteSerializer


def parse_platform(request):
    """
    Returns a PlatformModel instance based on the ID specified in the request.
    """
    return PlatformModel.objects.get(
        owner=request.user,
        id=request.data.get('platformId'))


def process_dates(request, game, dates):
    """
    Processes the list of new dates to add to a Game instance.
    Simply run a get_or_create() call with each provided date,
        just to make sure that that date exists.
    """
    if dates:
        for date in dates:
            GameDateRelation.objects.get_or_create(
                owner=request.user,
                date=date,
                game=game,
            )


def process_removed_dates(request, game, dates):
    """
    Processes the list of new dates to add to a Game instance.
    Simply run a get() call with each provided date,
        and delete any that are found.
    """
    if dates:
        for date in dates:
            gdr = GameDateRelation.objects.get(
                owner=request.user,
                date=date,
                game=game,
            )
            if gdr:
                gdr.delete()


class GameList(generics.ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Game.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GameReadSerializer
        if self.request.method == 'POST':
            return GameWriteSerializer

    def perform_create(self, serializer):
        game_instance = serializer.save(
            owner=self.request.user,
            platform=parse_platform(self.request))
        # create any new dates in the request
        process_dates(self.request, game_instance,
                      self.request.data.get('dates'))


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Game.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ('GET', 'DELETE'):
            return GameReadSerializer
        if self.request.method in ('PUT', 'PATCH'):
            return GameWriteSerializer

    def perform_update(self, serializer):
        # add platform info IF an ID is provided; if not, just leave it blank
        # this is to support both PUT and PATCH methods,
        # where the supplied data may be incomplete
        if self.request.data.get('platformId'):
            game_instance = serializer.save(
                platform=parse_platform(self.request))
        else:
            game_instance = serializer.save()

        # create any new dates in the request
        process_dates(self.request, game_instance,
                      self.request.data.get('dates'))
        # delete any dates that have been removed
        process_removed_dates(self.request, game_instance,
                              self.request.data.get('datesRemoved'))
