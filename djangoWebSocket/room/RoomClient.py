from room.RoomManager import room_manager
from room.RoomRequest import RoomRequest
from room.TournamentManager import tournament_manager
from room.UniqId import Uniqid


class RoomClient:
    session_id = ""
    session_expired = 0
    player_id = ""
    notif_id = ""
    in_a_room = False
    in_game = False
    in_a_room_tour = False
    in_game_tour = False
    waiting_time = 0
    final_waiting = False
    lang = ""
    channels = []
    obj = None
    active = False

    def __init__(self, obj):
        self.session_id = ""
        self.session_expired = 0
        self.player_id = ""
        self.notif_id = ""
        self.in_a_room = False
        self.in_game = False
        self.in_a_room_tour = False
        self.in_game_tour = False
        self.waiting_time = 0
        self.lang = "fr"
        self.channels = []
        self.obj = obj
        self.active = False
        self.final_waiting = False

    # ======= SETTER =======

    def setSessionId(self, session_id):
        self.session_id = session_id

    def setSessionExpired(self, session_expired):
        self.session_expired = session_expired

    def setPlayerId(self, player_id):
        self.player_id = player_id

    def setNotifId(self, notif_id):
        self.notif_id = notif_id

    def setInARoom(self, status):
        self.waiting_time = Uniqid.getUnixTimeStamp()
        self.in_a_room = status

    def setInGame(self, status):
        self.in_game = status

    def setInARoomTour(self, status):
        self.waiting_time = Uniqid.getUnixTimeStamp()
        self.in_a_room_tour = status

    def setInGameTour(self, status):
        self.in_game_tour = status

    def setLang(self, lang):
        self.lang = lang

    def setActive(self, status):
        self.active = status
    
    def setFinalWaiting(self, status):
        self.final_waiting = status

    async def addChannel(self, obj, channel):
        self.channels.append(channel)
        await obj.channel_layer.group_add(channel, obj.channel_name)

    async def removeChannel(self, obj, channel):
        self.channels.remove(channel)
        await obj.channel_layer.group_discard(channel, obj.channel_name)

    async def leaveChannel(self, obj, channel):
        await obj.channel_layer.group_discard(channel, obj.channel_name)

    # ======= GETTER =======

    def getSessionId(self):
        return self.session_id

    def getSessionExpired(self):
        return self.session_expired

    def getPlayerId(self):
        return self.player_id

    def getNotifId(self):
        return self.notif_id

    def isInARoom(self):
        return self.in_a_room

    def getInGame(self):
        return self.in_game

    def getInARoomTour(self):
        return self.in_a_room_tour

    def getInGameTour(self):
        return self.in_game_tour

    def getLang(self):
        return self.lang

    def getChannels(self):
        return self.channels

    def getObj(self):
        return self.obj

    def getActive(self):
        return self.active

    def getWaitingTime(self):
        result = Uniqid.getUnixTimeStamp() - self.waiting_time
        if result < 0 or result > 3600:
            result = 0
        return result

    # ======= OTHER =======

    def isAValidSession(self):
        if self.session_id != "":
            return True
        return False

    def printAll(self):
        print("Variables de RoomClient :")
        print(vars(self))
        pass

    async def updateChannel(self, obj):
        for channel in self.channels:
            await obj.channel_layer.group_discard(channel, obj.channel_name)
            await obj.channel_layer.group_add(channel, obj.channel_name)
        await self.actualState(obj)

    async def actualState(self, obj):
        for channel in self.channels:
            if room_manager.isRoomIdExist(channel):
                await RoomRequest.waitingMatch(obj, room_manager.getRoomById(channel).isWaiting())
                await RoomRequest.waitingTime(obj, self.getWaitingTime())
                await RoomRequest.joinStatusMatch(obj, True, room_manager.getRoomById(channel).getPlayerNb())
            elif tournament_manager.isTournamentIdExist(channel):
                await RoomRequest.waitingTour(channel, tournament_manager.getTournamentById(channel).isWaiting())
                await RoomRequest.waitingTime(obj, self.getWaitingTime())
                await RoomRequest.joinStatusTour(channel, True, tournament_manager.getTournamentById(channel).getPlayerNb())
        if self.final_waiting == True:
            await RoomRequest.tourFinalWaiting(obj)

