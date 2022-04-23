from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/league/', include('league.urls')),
    path('admin/', admin.site.urls),
]
