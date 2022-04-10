from django.db.models import Q
from django_filters import rest_framework as filters
from .models import Team, Game, Player


# Create filters for each field we want to be able to filter on Team
class TeamFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Team
        fields = ['name']


# Create filters for each field we want to be able to filter on Game
class GameFilter(filters.FilterSet):
    round = filters.CharFilter(lookup_expr='icontains')
    finished = filters.BooleanFilter()
    team = filters.NumberFilter(method='filter_both_teams')
    winner = filters.NumberFilter()

    class Meta:
        model = Game
        fields = ['round', 'finished', 'team', 'winner']

    # filter games played by the given team id either as home or away
    @staticmethod
    def filter_both_teams(queryset, name, value):
        return queryset.filter(
            Q(team_home=value) | Q(team_away=value)
        )


# create filters for each field we want to be able to filter on Player
class PlayerFilter(filters.FilterSet):
    team = filters.NumberFilter()
    games_played_gt = filters.NumberFilter(field_name='games_played', lookup_expr='gt')
    points_total_gt = filters.NumberFilter(field_name='points_total', lookup_expr='gt')
    points_average_gt = filters.NumberFilter(field_name='points_average', lookup_expr='gt')
    user_name = filters.CharFilter(method='filter_by_name')

    class Meta:
        model = Player
        fields = ['team', 'user_name', 'games_played_gt', 'points_total_gt', 'points_average_gt']

    # filter by the given name from username, first name or last name
    @staticmethod
    def filter_by_name(queryset, name, value):
        return queryset.filter(
            Q(user__username__icontains=value) | Q(user__first_name__icontains=value) | Q(
                user__last_name__icontains=value)
        )
