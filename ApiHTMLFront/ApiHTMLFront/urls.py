from django.contrib import admin
from django.urls import path, include
from .views import GameView, SignupView, LoginView, Fa2, GameOn, History, MatchHistory, Local

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('front/pong/', GameView.as_view(), name='pong'),
    path('front/signup/', SignupView.as_view(), name='signup'),
    path('front/login/', LoginView.as_view(), name='login'),
	path('front/2fa/', Fa2.as_view(), name='2fa'),
    path('front/game/on/', GameOn.as_view(), name='game'),
	path('front/game/local/', Local.as_view(), name='local'),
	path('front/history/<int:player_id>', History.as_view(), name='history'),
	path('front/history/get/<int:player_id>', MatchHistory),
]
