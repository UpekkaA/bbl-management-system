from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


# Season will be used when there are multiple seasons for the league.
class Season(models.Model):
    name = models.CharField(max_length=100)
    start = models.DateField(auto_now=True)  # in YYYY-MM-DD format
    end = models.DateField(auto_now=True)  # in YYYY-MM-DD format

    class Meta:
        ordering = ['-id']


# Stadium where the games are held
class Stadium(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    class Meta:
        ordering = ['-id']


# Team
class Team(models.Model):
    name = models.CharField(max_length=100)
    logo_url = models.CharField(max_length=100)
    games_played = models.PositiveSmallIntegerField(default=0)
    games_wins = models.PositiveSmallIntegerField(default=0)
    games_loses = models.PositiveSmallIntegerField(default=0)
    games_draws = models.PositiveSmallIntegerField(default=0)
    points_total = models.PositiveBigIntegerField(default=0)
    points_average = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('auth.User', related_name='teams', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']


# Player
# Once the player is registered, the generated id will be used for unique identification
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    height = models.PositiveSmallIntegerField(default=0)
    games_played = models.PositiveSmallIntegerField(default=0)
    points_total = models.PositiveBigIntegerField(default=0)
    points_average = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']


# Coach
# One team can have more than one coach
class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']


# Game, when a match is scheduled , the entry is added.
# After the match is completed, the results will be updated.
class Game(models.Model):
    # define enum for the available rounds
    class Round(models.TextChoices):
        QUALIFIER = 'QU', _('Qualifier')
        QUARTER_FINAL = 'QF', _('Quarter Final')
        SEMI_FINAL = 'SF', _('Semi Final')
        FINAL = 'FI', _('Final')

    date_time = models.DateTimeField(auto_now_add=False)
    stadium = models.ForeignKey(Stadium, related_name='games', on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)
    round = models.CharField(
        max_length=2,
        choices=Round.choices,
        default=Round.QUALIFIER,
    )
    # season = models.ForeignKey(Season, related_name='games', on_delete=models.CASCADE)
    team_home = models.ForeignKey(Team, related_name='games_home', on_delete=models.CASCADE)
    team_away = models.ForeignKey(Team, related_name='games_away', on_delete=models.CASCADE)
    winner = models.ForeignKey(Team, null=True, blank=True, default=None, related_name='games_winner',
                               on_delete=models.CASCADE)
    score_home = models.PositiveSmallIntegerField(default=0)
    score_away = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('auth.User', related_name='games', on_delete=models.CASCADE)

    players = models.ManyToManyField(Player)

    class Meta:
        ordering = ['-id']

