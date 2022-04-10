from django.contrib.auth.models import User, Group
from rest_framework import generics, viewsets, permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.templatetags import rest_framework
from django_filters import rest_framework as filters

from .filters import TeamFilter
from .models import Team, Stadium
from .pagination import CustomPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import RegisterSerializer, UserSerializer, GroupSerializer, TeamSerializer, StadiumSerializer


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
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
