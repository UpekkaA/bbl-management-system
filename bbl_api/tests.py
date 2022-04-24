from django.contrib.auth.models import User
from rest_framework import status

from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.test import force_authenticate

from league.models import Team, Player, Game, Stadium
from league.views import ListCreateTeamAPIView, GamePlayerAPIView


class PlayerTests(APITestCase):

    def test_create_admin_user(self):
        """
        Ensure we can create a new admin user.
        """
        url = '/api/v1/auth/register/'
        data = {
            'username': 'admin',
            'password': 'Bbl@4321',
            'email': 'admin@bbltestdjango.com',
            'first_name': 'Admin',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'admin')

    def test_create_team(self):
        """
        Ensure we can create a new team.
        """
        url = '/api/v1/league/teams'
        data = {
            'name': 'Tasmania JackJumpers',
            'logo_url': 'https://source.unsplash.com/user/c_v_r/100x100'
        }

        factory = APIRequestFactory()
        user = User.objects.create(username='admin')
        view = ListCreateTeamAPIView.as_view()

        # Make an authenticated request to the view...
        request = factory.post(url, data, format='json')
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(Team.objects.get().name, 'Tasmania JackJumpers')

    def test_get_teams(self):
        """
        Ensure we can list teams
        """
        url = '/api/v1/league/teams'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        """
        Ensure we can create a new user.
        """
        url = '/api/v1/auth/register/'
        data = {
            'username': 'victor',
            'password': 'Bbl@4321',
            'email': 'victor@bbltestdjango.com',
            'first_name': 'Victor',
            'last_name': 'Law'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'victor')

    def test_get_players(self):
        """
        Ensure we can list players
        """
        url = '/api/v1/league/players'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_listing_players(self):
        """
        Ensure we can list players
        """
        url = '/api/v1/league/players?percentile=90'
        admin_user = User.objects.create(username='admin')
        player_user_1 = User.objects.create(username='john', first_name='John', last_name='Doe')
        player_user_2 = User.objects.create(username='alex', first_name='Alex', last_name='Law')
        team = Team.objects.create(name='Tasmania JackJumpers',
                                   logo_url='https://source.unsplash.com/user/c_v_r/100x100', creator=admin_user)
        Player.objects.create(user=player_user_1, team=team, height=180,
                              games_played=12, points_total=240, points_average=20)
        Player.objects.create(user=player_user_2, team=team, height=190,
                              games_played=15, points_total=450, points_average=30)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_game_player(self):
        """
        Ensure we can list game players
        """
        url = '/api/v1/league/games/players?team=1&game=1'
        admin_user = User.objects.create(username='admin')
        player_user_1 = User.objects.create(username='john', first_name='John', last_name='Doe')
        player_user_2 = User.objects.create(username='alex', first_name='Alex', last_name='Law')
        team_1 = Team.objects.create(name='Tasmania JackJumpers',
                                     logo_url='https://source.unsplash.com/user/c_v_r/100x100', creator=admin_user)
        team_2 = Team.objects.create(name='Sydney Titans',
                                     logo_url='https://source.unsplash.com/user/c_v_r/100x100', creator=admin_user)
        player_1 = Player.objects.create(user=player_user_1, team=team_1, height=180,
                                         games_played=12, points_total=240, points_average=20)
        player_2 = Player.objects.create(user=player_user_2, team=team_2, height=190,
                                         games_played=15, points_total=450, points_average=30)
        stadium = Stadium.objects.create(name='Sydney Complex', location='Sydney')
        game_players = [player_1, player_2]
        game = Game.objects.create(date_time='2022-05-10 08:00:00.000000', stadium=stadium, round=Game.Round.QUALIFIER,
                                   team_home=team_1, team_away=team_2, creator=admin_user)
        game.players.set(game_players)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_game_players(self):
        """
        Ensure we can save game players
        """
        url = '/api/v1/league/games/players?team=1&game=1'
        data = {
            'team_id': 1,
            'game_id': 1,
            'player_ids': [1, 2]
        }
        admin_user = User.objects.create(username='admin')
        player_user_1 = User.objects.create(username='john', first_name='John', last_name='Doe')
        player_user_2 = User.objects.create(username='alex', first_name='Alex', last_name='Law')
        team_1 = Team.objects.create(name='Tasmania JackJumpers',
                                     logo_url='https://source.unsplash.com/user/c_v_r/100x100', creator=admin_user)
        team_2 = Team.objects.create(name='Sydney Titans',
                                     logo_url='https://source.unsplash.com/user/c_v_r/100x100', creator=admin_user)
        Player.objects.create(user=player_user_1, team=team_1, height=180,
                                         games_played=12, points_total=240, points_average=20)
        Player.objects.create(user=player_user_2, team=team_2, height=190,
                                         games_played=15, points_total=450, points_average=30)
        stadium = Stadium.objects.create(name='Sydney Complex', location='Sydney')
        Game.objects.create(date_time='2022-05-10 08:00:00.000000', stadium=stadium, round=Game.Round.QUALIFIER,
                                   team_home=team_1, team_away=team_2, creator=admin_user)
        factory = APIRequestFactory()
        view = GamePlayerAPIView.as_view()

        # Make an authenticated request to the view...
        request = factory.post(url, data, format='json')
        force_authenticate(request, user=admin_user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
