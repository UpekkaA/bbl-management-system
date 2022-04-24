import logging

from django.contrib.auth.models import User, Group
from django_filters import rest_framework as filters
from rest_framework import generics, viewsets, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import TeamFilter, GameFilter, PlayerFilter
from .models import Team, Stadium, Game, Coach, Player
from .pagination import CustomPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import GroupSerializer, TeamSerializer, StadiumSerializer, \
    GameSerializer, CoachSerializer, PlayerSerializer

import pandas as pd

logger = logging.getLogger(__name__)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ListCreateStadiumAPIView(ListCreateAPIView):
    """
    API endpoint that allows stadiums to be viewed or edited.
    """
    serializer_class = StadiumSerializer
    queryset = Stadium.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Assign the user who created the team
        serializer.save()


class RetrieveUpdateDestroyStadiumAPIView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows stadiums to be viewed or edited.
    """
    serializer_class = StadiumSerializer
    queryset = Stadium.objects.all()
    permission_classes = [IsAuthenticated]


class ListCreateTeamAPIView(ListCreateAPIView):
    """
    API endpoint that allows teams to be viewed or edited.
    """
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = (AllowAny,)
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TeamFilter

    def perform_create(self, serializer):
        # Assign the user who created the team
        logger.info("Info: Perform create Team")
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyTeamAPIView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows teams to be viewed or edited.
    """
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class ListCreateGameAPIView(ListCreateAPIView):
    """
    API endpoint that allows games to be viewed or edited.
    """
    serializer_class = GameSerializer
    queryset = Game.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = GameFilter

    def perform_create(self, serializer):
        # Assign the user who created the team
        logger.info("Info: Perform create Game")
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyGameAPIView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows games to be viewed or edited.
    """
    serializer_class = GameSerializer
    queryset = Game.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class ListCreateCoachAPIView(ListCreateAPIView):
    """
    API endpoint that allows Coaches to be viewed or edited.
    """
    serializer_class = CoachSerializer
    queryset = Coach.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        logger.info("Info: Perform create Coach")
        serializer.save()


class RetrieveUpdateDestroyCoachAPIView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows Coaches to be viewed or edited.
    """
    serializer_class = CoachSerializer
    queryset = Coach.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class ListCreatePlayerAPIView(ListCreateAPIView):
    """
    API endpoint that allows Players to be viewed or edited.
    """
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PlayerFilter

    def perform_create(self, serializer):
        logger.info("Info: Perform create Player")
        serializer.save()


class RetrieveUpdateDestroyPlayerAPIView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows Players to be viewed or edited.
    """
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class GamePlayerAPIView(APIView):
    """
    API endpoint that allows Players to be selected for the games,
    The coach will select the team members who will play for each game.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        logger.info("Info: View Player Selection for Game")
        team_id = request.query_params.get('team')
        game_id = request.query_params.get('game')

        if game_id is not None:
            game = Game.objects.get(id=game_id)
            if game is not None:
                players = list(game.players.values())
                if team_id is not None:
                    team = Team.objects.get(id=team_id)
                    if team is not None:
                        team_players = list()
                        for p in players:
                            if p['team_id'] == int(team_id):
                                team_players.append(p)
                        players = list(team_players)
                player_df = pd.DataFrame(players)
                if player_df.empty:
                    return Response(list(), status=status.HTTP_200_OK)
                players_ids = list(player_df['id'])
                return Response(players_ids, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        logger.info("Info: Perform Player Selection for Game")
        team_id = request.data.get('team_id')
        game_id = request.data.get('game_id')
        player_ids = request.data.get('player_ids')

        if game_id is not None:
            game = Game.objects.get(id=game_id)
            if game is not None:
                game_players = list()
                if team_id is not None:
                    team = Team.objects.get(id=team_id)
                    if team is not None:
                        for p in player_ids:
                            player = Player.objects.get(id=p)
                            if player is not None and player.team_id == int(team_id):
                                game_players.append(player)

                game.players.set(game_players)
                game.save()
                return Response(game, status=status.HTTP_201_CREATED)

        return Response(None, status=status.HTTP_400_BAD_REQUEST)
