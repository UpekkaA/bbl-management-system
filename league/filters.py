from django_filters import rest_framework as filters
from .models import Team


# We create filters for each field we want to be able to filter on
class TeamFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Team
        fields = ['name']

