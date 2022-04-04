from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100)
    logo_url = models.CharField(max_length=100)
    games_played = models.PositiveSmallIntegerField(default=0)
    games_wins = models.PositiveSmallIntegerField(default=0)
    games_losses = models.PositiveSmallIntegerField(default=0)
    points = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('auth.User', related_name='teams', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
