import json

from channels.generic.websocket import AsyncWebsocketConsumer

from language.Language import language
from notification.ClientManager import client_manager
from notification.Request import Request
from notification.Client import Client
from notification.Signature import Signature


class Consumer(AsyncWebsocketConsumer):
    notif_group_name = "notif_lobby"
    client = None

    """
    SOCKET EVENT:
    """
    async def connect(self):
        print("[NOTIF] New connection")
        await self.accept()
        self.client = Client(self)
        await self.client.addChannel(self, self.notif_group_name)
        await Request.connection(self)

    async def disconnect(self, close_code):
        print("[NOTIF] Leave connection")
        await self.client.leaveChannel(self, self.notif_group_name)
        if self.client.getPlayerId() != "":
            client_manager.removeClient(self.client.getPlayerId())

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data["type"] == "auth":
            await self.clientAuth(data["session_id"], data["player_id"])
            return
        if data["type"] == "disconnect":
            self.client = Client(self)
            return
        if data["type"] == "lang" and self.client.getPlayerId() != "":
            self.client.setLang(data["language"])
            return

    """
    AUTHENTIFY:

    Client need (valid auth)
    """
    async def clientAuth(self, session_id, player_id):
        if session_id != "":  # Auth API check
            if self.client.getPlayerId() == "":
                client_manager.addClient(self.client)
            self.client.setSessionId(session_id)
            self.client.setPlayerId(player_id)
            return

    async def sendToGroup(self, event):
        event_data = event.copy()
        rq_type = event_data.pop('rq_type')
        event_data['type'] = str(rq_type)
        print(event_data)
        await self.send(text_data=json.dumps(event_data))
