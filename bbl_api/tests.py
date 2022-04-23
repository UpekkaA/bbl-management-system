from django.contrib.auth.models import User
from rest_framework import status

from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.test import force_authenticate

from league.models import Team, Player
from league.views import ListCreateTeamAPIView


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
