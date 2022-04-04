from django.urls import path

from league import views

urlpatterns = [

    # Teams
    path('teams', views.ListCreateTeamAPIView.as_view(), name='get_post_teams'),
    path('teams/<int:pk>/', views.RetrieveUpdateDestroyTeamAPIView.as_view(), name='get_delete_update_teams'),
]

