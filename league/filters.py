from django_filters import rest_framework as filters
from .models import Team, Game


# We create filters for each field we want to be able to filter on
class TeamFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Team
        fields = ['name']


# We create filters for each field we want to be able to filter on
class GameFilter(filters.FilterSet):
    round = filters.CharFilter(lookup_expr='icontains')
    finished = filters.BooleanFilter()
    year = filters.NumberFilter()
    year__gt = filters.NumberFilter(field_name='year', lookup_expr='gt')
    year__lt = filters.NumberFilter(field_name='year', lookup_expr='lt')
    creator__username = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Game
        fields = ['round', 'finished', 'year', 'year__gt', 'year__lt', 'creator__username']
