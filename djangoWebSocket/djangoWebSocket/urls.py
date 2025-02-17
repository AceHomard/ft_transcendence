"""
URL configuration for djangoWebSocket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

import api.views
import room.views
import game.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', room.views.lobby),
    path('mm/debug_room', room.views.debug_room),
    path('mm/debug_client', room.views.debug_client),
    path('mm/debug_tournament', room.views.debug_tournament),
    path('api/match_result/', api.views.match_result),
    path('cli/command/', game.views.command_view)
]
