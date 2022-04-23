from django.contrib.auth.models import Group
from rest_framework import serializers

from league.models import Team, Stadium, Game, Coach, Player


# Serializers
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


# create class to serializer model for Stadium
class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = ('id', 'name', 'location')


# create class to serializer model for Team
class TeamSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Team
        fields = ('id', 'name', 'logo_url', 'creator')


# create class to serializer model for Game
class GameSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Game
        fields = ('id', 'date_time', 'stadium', 'finished', 'round', 'team_home', 'team_away', 'winner', 'score_home',
                  'score_away', 'creator')


# create class to serializer model for Coach
class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = ('user', 'team')


# create class to serializer model for Player
class PlayerSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    team_name = serializers.ReadOnlyField(source='team.name')

    class Meta:
        model = Player
        fields = (
            'user', 'team', 'height', 'games_played', 'points_total', 'points_average', 'username', 'first_name',
            'last_name', 'team_name')
