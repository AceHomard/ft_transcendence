import json

from channels.generic.websocket import AsyncWebsocketConsumer
from language.Language import language
from room.RoomManager import room_manager
from room.RoomClient import RoomClient
from room.RoomRequest import RoomRequest
from room.RoomClientManager import room_client_manager
from room.TournamentManager import tournament_manager
from api.PostRequest import post_request
from room.UniqId import Uniqid
from room.Social import *
from game.GameManager import game_manager

class RoomConsumer(AsyncWebsocketConsumer):
    room_group_name = "room_lobby"
    client = None

    """
    SOCKET EVENT:
    """
    async def connect(self):
        print("[ROOM] New connection")
        await self.accept()
        self.client = RoomClient(self)
        await self.client.addChannel(self, self.room_group_name)
        await RoomRequest.connection(self)

    async def disconnect(self, close_code):
        print("[ROOM] Leave connection")
        await self.client.leaveChannel(self, self.room_group_name)
        self.client.setActive(False)
        await leaveClient(self.client.getPlayerId())

    async def receive(self, text_data):
        data = json.loads(text_data)

        if "action" in data:
            action = data.get('action')
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
                return

        if data["type"] == "auth":
            await self.clientAuth(data["session_id"], data["player_id"], data["notif_id"])
            return
        if data["type"] == "disconnect":
            await self.client.leaveChannel(self, self.room_group_name)
            self.client.setActive(False)
            await leaveClient(self.client.getPlayerId())
            self.client = RoomClient(self)
            return
        if data["type"] == "social":
            if data["category"] == "add_friend":
                await addFriend(self.client.getPlayerId(), data["user_id"])
            elif data["category"] == "remove_friend":
                await removeFriend(self.client.getPlayerId(), data["user_id"])
            return
        if data["type"] == "matchmaking":
            await self.clientMatchmaking(data)
            return
        if data["type"] == "client_status":
            await self.client.actualState(self)
            return

    """
    AUTHENTIFY:
    
    Client need (valid auth)
    """
    async def clientAuth(self, session_id, player_id, notif_id):
        self.client.setNotifId(notif_id)

        if self.client.isAValidSession():
            self.client.obj = self
            self.client.setActive(True)
            await joinClient(self.client.getPlayerId())
            return

        if room_client_manager.isClientIdExist(session_id):
            self.client = room_client_manager.getClientById(session_id)
            if self.client.getActive() == True:
                await RoomRequest.notification(self, "error", "error_auth_invalid", "error_auth_invalid")
                return
            await self.client.updateChannel(self)
            self.client.obj = self
            self.client.setActive(True)
            await joinClient(self.client.getPlayerId())
            games = game_manager.getAllGames()
            for game in games:
                if game.playerIsInGame(player_id):
                    await game.syncGameState(player_id)
            return

        if post_request.APIvalidAuth(player_id) == True:  # Auth API check
            self.client.setSessionId(session_id)
            self.client.setPlayerId(player_id)
            room_client_manager.addClient(self.client)
            self.client.setActive(True)
            await joinClient(self.client.getPlayerId())
            await self.checkIfIsGame(player_id)
            return
        post_request.pushNotif({"user_id":self.client.getNotifId(),"status":"error","title":"notif.error.title","message":"notif.error.invalid_auth"})
        await RoomRequest.notification(self, "error", "error_auth_invalid", "error_auth_invalid")


    """
    MATCHMAKING:

    Client need (valid auth / not in game / not waiting)
    """
    async def clientMatchmaking(self, data):
        lang = self.client.getLang()
        if not self.client.isAValidSession():
            await RoomRequest.notification(self, "error", "Fatal Error", "Login redirection")
            return

        if data["action"] == "cancel":
            await self.mm_cancel()
            return

        if self.client.getInGame() or self.client.getInGameTour():
            post_request.pushNotif({"user_id":self.client.getNotifId(),"status":"error","title":"notif.error.title","message":"notif.error.already_in_game"})
            return
        if self.client.isInARoom():
            post_request.pushNotif({"user_id":self.client.getNotifId(),"status":"error","title":"notif.error.title","message":"notif.error.already_waiting_room"})
            return
        if self.client.getInARoomTour():
            post_request.pushNotif({"user_id":self.client.getNotifId(),"status":"error","title":"notif.error.title","message":"notif.error.already_waiting_tournament"})
            return

        if data["action"] == "find_game":
            if data["ia_game"] == "true":
                await self.botGame()
            else:
                await self.mm_findGame()
        elif data["action"] == "find_tournament":
            await self.mm_findTournament()

    """
    CANCEL MATCHMAKING:

    Client need (depend on clientMatchmaking)
    """
    async def mm_cancel(self):
        if self.client.isInARoom():
            waiting_room = room_manager.getWaitingRoom()
            if waiting_room is not False:
                room = room_manager.getRoomById(waiting_room)
                if room.playerIdIsInRoom(self.client.getPlayerId()):
                    await RoomRequest.mmCanceled(self)
                    self.client.setInARoom(False)
                    await self.client.removeChannel(self, waiting_room)
                    room_manager.removeRoomById(waiting_room)
            return

        if self.client.getInARoomTour():
            #check si le tournoi n'a pas deja commence
            waiting_tour = tournament_manager.getWaitingTournament()
            if waiting_tour is not False:
                tour = tournament_manager.getTournamentById(waiting_tour)
                if tour.playerIsInTournament(self.client.getPlayerId()):
                    await RoomRequest.mmCanceled(self)
                    self.client.setInARoomTour(False)
                    await self.client.removeChannel(self, waiting_tour)
                    tour.removePlayer(self.client.getPlayerId())
                    await RoomRequest.joinStatusTour(waiting_tour, True, tour.getPlayerNb())
                    if (tour.getPlayerNb() == 0):
                        tournament_manager.removeTournamentById(waiting_tour)
            return

    """
    FIND TOURNAMENT:

    Client need (depend on clientMatchmaking)
    """
    async def mm_findTournament(self):
        waiting_tour = tournament_manager.getWaitingTournament()

        if waiting_tour is False:
            waiting_tour = tournament_manager.createTournament()
            await self.clientJoinTournament(waiting_tour, self.client.getPlayerId())
            self.client.setInARoomTour(True)
            await RoomRequest.waitingTour(waiting_tour, True)
            await RoomRequest.waitingTime(self, self.client.getWaitingTime())

        else:
            if await self.clientJoinTournament(waiting_tour, self.client.getPlayerId()):
                self.client.setInARoomTour(True)
                if tournament_manager.getTournamentById(waiting_tour).getPlayerNb() == 4:
                    await tournament_manager.getTournamentById(waiting_tour).startTournament()
                    self.client.setInGameTour(True)
                    await RoomRequest.waitingTour(waiting_tour, False)
                else:
                    await RoomRequest.waitingTour(waiting_tour, True)
                    await RoomRequest.waitingTime(self, self.client.getWaitingTime())

    """
    BOT MATCH:
    
    Client need (depend on clientMatchmaking)
    """
    async def botGame(self):
        bot_id = Uniqid.generate()
        client_bot = RoomClient(self)
        client_bot.setSessionId(bot_id)
        client_bot.setPlayerId(bot_id)
        client_bot.setNotifId(bot_id)
        room_client_manager.addClient(client_bot)

        waiting_room = room_manager.createRoom()
        await self.clientJoinRoom(waiting_room, self.client.getPlayerId())
        self.client.setInARoom(True)
        await self.clientJoinRoom(waiting_room, bot_id)
        client_bot.setInARoom(True)
        room_manager.getRoomById(waiting_room).setGameIa(True)
        #await RoomRequest.waitingMatch(self.client.getObj(), True, room_manager.getRoomById(waiting_room).getPlayerNb())
        #await RoomRequest.waitingMatch(client_bot.getObj(), True, room_manager.getRoomById(waiting_room).getPlayerNb())
        await RoomRequest.waitingMatch(self.client.getObj(), True)
        await RoomRequest.waitingMatch(client_bot.getObj(), True)
        post_request.addPostBot({"bot_id": bot_id})
        await room_manager.getRoomById(waiting_room).setGameStarted()
        room_manager.getRoomById(waiting_room).setAllPlayersInGameStatus(True)


    """
    FIND MATCH:
    
    Client need (depend on clientMatchmaking)
    """
    async def mm_findGame(self):
        waiting_room = room_manager.getWaitingRoom()

        if waiting_room is False:
            waiting_room = room_manager.createRoom()
            await self.clientJoinRoom(waiting_room, self.client.getPlayerId())
            self.client.setInARoom(True)
            await RoomRequest.waitingMatch(self.client.getObj(), True)
            await RoomRequest.waitingTime(self, self.client.getWaitingTime())
        else:
            if await self.clientJoinRoom(waiting_room, self.client.getPlayerId()):
                room = room_manager.getRoomById(waiting_room)
                await room.setGameStarted()
                self.client.setInARoom(True)
                await RoomRequest.foundMatch(waiting_room, waiting_room)

                player_a = room_client_manager.getClientById(room.getPlayerA())
                player_b = room_client_manager.getClientById(room.getPlayerB())
                if player_a != False:
                    await RoomRequest.waitingMatch(player_a.getObj(), False)
                if player_b != False:
                    await RoomRequest.waitingMatch(player_b.getObj(), False)
                room.setAllPlayersInGameStatus(True)

    """
    JOIN TOURNAMENT:

    Client need (valid auth / not in tour / not already in this tour)
    """
    async def clientJoinTournament(self, tour_id, player_id):
        lang = self.client.getLang()
        if not self.client.isAValidSession():
            await RoomRequest.notification(self, "error", "Fatal Error", "Login redirection")
            return False

        if not tournament_manager.isTournamentIdExist(tour_id):
            post_request.pushNotif({"user_id":self.client.getNotifId(),"status":"error","title":"notif.error.title","message":"notif.error.unknown_in_tournament"})
            return False

        tour = tournament_manager.getTournamentById(tour_id)
        if tour.playerIsInTournament(player_id):
            post_request.pushNotif({"user_id":self.client.getNotifId(),"status":"error","title":"notif.error.title","message":"notif.error.already_in_tournament"})
            return False

        if not tour.addPlayer(player_id):
            post_request.pushNotif({"user_id":self.client.getNotifId(),"status":"error","title":"notif.error.title","message":"notif.error.tournament_full"})
            return False
        await self.client.addChannel(self, tour_id)
        await RoomRequest.joinStatusTour(tour_id, True, tour.getPlayerNb())
        return True

    """
    JOIN ROOM:
    
    Client need (valid auth / not in game / not already in this room)
    """
    async def clientJoinRoom(self, room_id, player_id):
        lang = self.client.getLang()

        if not self.client.isAValidSession():
            await RoomRequest.notification(self, "error", "Fatal Error", "Login redirection")
            return False

        if not room_manager.isRoomIdExist(room_id):
            post_request.pushNotif({"user_id":self.client.getNotifId(),"status":"error","title":"notif.error.title","message":"notif.error.unknown_in_room"})
            return False

        room = room_manager.getRoomById(room_id)
        if room.playerIdIsInRoom(player_id):
            post_request.pushNotif({"user_id":self.client.getNotifId(),"status":"error","title":"notif.error.title","message":"notif.error.already_in_room"})
            return False

        if not room.addPlayer(player_id):
            post_request.pushNotif({"user_id":self.client.getNotifId(),"status":"error","title":"notif.error.title","message":"notif.error.game_full"})
            return False

        await self.client.addChannel(self, room_id)
        if room.getPlayerA() != "":
            await RoomRequest.joinStatusMatch(room_client_manager.getClientById(room.getPlayerA()).getObj(), True, room.getPlayerNb())
        if room.getPlayerB() != "":
            await RoomRequest.joinStatusMatch(room_client_manager.getClientById(room.getPlayerB()).getObj(), True, room.getPlayerNb())
        return True

    """
    JOIN CHANNEL GAME:

    Client need (valid auth)
    """
    async def checkIfIsGame(self, player_id):
        print("*******************")
        if not self.client.isAValidSession():
            return
        games = game_manager.getAllGames()
        for game in games:
            print(player_id, game.getPlayerAId(), game.getPlayerBId())
            if not game.isReady():
                if not game.player_a_connected and str(game.getPlayerAId()) == str(player_id):
                    print("***** game.connectPlayerA()")
                    await game.connectPlayerA()
                elif str(game.getPlayerBId()) == str(player_id):
                    print("***** game.connectPlayerB()")
                    await game.connectPlayerB()
                if game.isReady():
                    print("***** game.gameStart()")
                    await game.gameStart()


    async def sendToGroup(self, event):
        event_data = event.copy()
        if "rq_type" in event_data:
            rq_type = event_data.pop('rq_type')
            event_data['type'] = str(rq_type)

        await self.send(text_data=json.dumps(event_data))

    async def sendToGroupGame(self, event):
        event_data = event.copy()
        event_data.pop('type')
        await self.send(text_data=json.dumps(event_data))