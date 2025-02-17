from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
import json
from .bot import BotManager


@api_view(['POST'])
def create_bot(request):
    data = json.loads(request.body)
    bot = BotManager()
    bot.addBot(data.get('bot_id'))
    return JsonResponse({'Success': True})
    
# Create your views here.