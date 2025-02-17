import time, asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from game.Client import Client
from game.ClientManager import client_manager
from game.ConsumerRequest import ConsumerRequest
from game.GameManager import game_manager
# pong/consumers.py

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 320
PLAYER_HEIGHT = 50

class PongConsumer(AsyncWebsocketConsumer):
	client = None
	async def connect(self):
		await self.accept()
		self.client = Client(self)
		await ConsumerRequest.connection(self)

	async def disconnect(self, close_code):
		pass

	async def receive(self, text_data):
		data = json.loads(text_data)
		action = data.get('action')
		
		if action == 'auth':
			await self.clientAuth(data.get('player_id'))
			return
		if action == "disconnect":
			self.client = Client(self)
			return
		if action == 'move_paddle':
			if not game_manager.clientIsInGame(self.client.player_id):
				return
			game_id = game_manager.getClientInGame(self.client.player_id)
			mouvement = data.get('mouvement')
			if not game_manager.ifGameExist(game_id):
				print('game does not exist')
				return
			game = game_manager.getGameById(game_id)
			if not game.playerIsInGame(self.client.player_id):
				print('player not in game')
				return
			await game.move_paddle(self.client.player_id, mouvement)

	"""
	AUTHENTIFY:

	Client need (valid auth)
	"""
	async def clientAuth(self, player_id):
		print(player_id)
		if self.client.isAValidSession():
			return

		if client_manager.isClientIdExist(player_id):
			self.client = client_manager.getClientById(player_id)
			self.client.obj = self
			await self.client.updateChannel(self)
			games = game_manager.getAllGames()
			for game in games:
				if game.playerIsInGame(player_id):
					await game.syncGameState(player_id)
			return

		if player_id != "":  # Auth API check
			self.client.setPlayerId(player_id)
			client_manager.addClient(self.client)
			await self.checkIfIsGame(player_id)
			return

	"""
	JOIN CHANNEL GAME:

	Client need (valid auth)
	"""
	async def checkIfIsGame(self, player_id):
		if not self.client.isAValidSession():
			return
		games = game_manager.getAllGames()
		for game in games:
			if not game.isReady():
				if not game.player_a_connected and str(game.getPlayerAId()) == str(player_id):
					await game.connectPlayerA()
				elif str(game.getPlayerBId()) == str(player_id):
					await game.connectPlayerB()
				if game.isReady():
					await game.gameStart()

	async def sendToGroupGame(self, event):
		event_data = event.copy()
		event_data.pop('type')
		await self.send(text_data=json.dumps(event_data))