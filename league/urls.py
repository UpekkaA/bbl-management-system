from django.urls import path

from league import views

urlpatterns = [

    # Teams
    path('teams', views.ListCreateTeamAPIView.as_view(), name='get_post_teams'),
    path('teams/<int:pk>/', views.RetrieveUpdateDestroyTeamAPIView.as_view(), name='get_delete_update_teams'),

    # Teams
    path('games', views.ListCreateGameAPIView.as_view(), name='get_post_games'),
    path('games/<int:pk>/', views.RetrieveUpdateDestroyGameAPIView.as_view(), name='get_delete_update_games'),

    # Stadiums
    path('stadiums', views.ListCreateStadiumAPIView.as_view(), name='get_post_stadiums'),
    path('stadiums/<int:pk>/', views.RetrieveUpdateDestroyStadiumAPIView.as_view(), name='get_delete_update_stadiums'),

    # Coaches
    path('coaches', views.ListCreateCoachAPIView.as_view(), name='get_post_coaches'),
    path('coaches/<int:pk>/', views.RetrieveUpdateDestroyCoachAPIView.as_view(), name='get_delete_update_coaches'),

    # Player
    path('players', views.ListCreatePlayerAPIView.as_view(), name='get_post_player'),
    path('players/<int:pk>/', views.RetrieveUpdateDestroyPlayerAPIView.as_view(), name='get_delete_update_player'),

    # TODO: Seasons
    # path('seasons', views.ListCreateSeasonsAPIView.as_view(), name='get_post_teams'),
    # path('seasons/<int:pk>/', views.RetrieveUpdateDestroySeasonsAPIView.as_view(), name='get_delete_update_teams'),
]
