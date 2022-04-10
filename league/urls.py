from django.urls import path

from league import views

urlpatterns = [

    # Seasons
    # path('seasons', views.ListCreateSeasonsAPIView.as_view(), name='get_post_teams'),
    # path('seasons/<int:pk>/', views.RetrieveUpdateDestroySeasonsAPIView.as_view(), name='get_delete_update_teams'),

    # Teams
    path('teams', views.ListCreateTeamAPIView.as_view(), name='get_post_teams'),
    path('teams/<int:pk>/', views.RetrieveUpdateDestroyTeamAPIView.as_view(), name='get_delete_update_teams'),

    # Stadiums
    path('stadiums', views.ListCreateStadiumAPIView.as_view(), name='get_post_teams'),
    path('stadiums/<int:pk>/', views.RetrieveUpdateDestroyStadiumAPIView.as_view(), name='get_delete_update_teams'),
]

