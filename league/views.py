from django.contrib.auth.models import User, Group
from django_filters import rest_framework as filters
from rest_framework import generics, viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly

from .filters import TeamFilter, GameFilter
from .models import Team, Stadium, Game
from .pagination import CustomPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import RegisterSerializer, UserSerializer, GroupSerializer, TeamSerializer, StadiumSerializer, \
    GameSerializer


class RegisterView(generics.CreateAPIView):
    """
    API endpoint that allows users to be registered.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = (AllowAny,)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)
    # permission_classes = [permissions.IsAuthenticated]


class ListCreateStadiumAPIView(ListCreateAPIView):
    """
    API endpoint that allows stadiums to be viewed or edited.
    """
    serializer_class = StadiumSerializer
    queryset = Stadium.objects.all()
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]
    # permission_classes = (AllowAny,)
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TeamFilter

    def perform_create(self, serializer):
        # Assign the user who created the team
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
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyGameAPIView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows games to be viewed or edited.
    """
    serializer_class = GameSerializer
    queryset = Game.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
