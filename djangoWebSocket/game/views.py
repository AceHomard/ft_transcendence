from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from game.Game import Game
from game.GameManager import game_manager
import json

@csrf_exempt
def command_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cookie = request.COOKIES.get('uniqid')
        if not game_manager.clientIsInGame(cookie):
            return JsonResponse({'status': 'error', 'message': 'cookie not in game'}, status=400)
        game_id = game_manager.getClientInGame(cookie)
        mouvement = data.get('mouvement')
        if not game_manager.ifGameExist(game_id):
            print('game does not exist')
            return JsonResponse({'status': 'error', 'message': 'game do not exist'}, status=400)
        game = game_manager.getGameById(game_id)
        if not game.playerIsInGame(cookie):
            print('player not in game')
            return JsonResponse({'status': 'error', 'message': 'player not in game'}, status=400)
        game.move_api_paddle(cookie, mouvement)
        return JsonResponse({'status': 'success'}, status=207)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)