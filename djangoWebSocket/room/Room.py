import uuid
import time

from api.PostRequest import PostRequest, post_request
from room.RoomClientManager import room_client_manager
from game.ClientManager import client_manager
from room.RoomRequest import RoomRequest
from room.UniqId import Uniqid
import requests
from .loger_config import setup_logger
from game.GameManager import game_manager

logger = setup_logger(__name__)

class Room:
    id = 0
    player_id_a = ""
    player_id_b = ""
    score_player_a = 0
    score_player_b = 0
    game_start_date = 0
    game_end_date = 0
    created_date = 0
    game_started = False
    game_ia = False

    def __init__(self):
        self.id = Uniqid.generate()
        self.player_id_a = ""
        self.player_id_b = ""
        self.score_player_a = 0
        self.score_player_b = 0
        self.game_start_date = 0
        self.game_end_date = 0
        self.created_date = Uniqid.getUnixTimeStamp()
        self.game_started = False
        self.game_ia = False

    # ======= SETTER =======

    def setPlayerA(self, player_id_a):
        self.player_id_a = player_id_a

    def setPlayerB(self, player_id_b):
        self.player_id_b = player_id_b

    def setScorePlayerA(self, score_player_a):
        self.score_player_a = score_player_a

    def setScorePlayerB(self, score_player_b):
        self.score_player_b = score_player_b

    def setGameStartDate(self):
        self.game_start_date = int(time.time())

    def setGameEndDate(self):
        self.game_end_date = int(time.time())

    def addPlayer(self, player_id):
        if self.getPlayerNb() == 2:
            return False
        if self.getPlayerNb() == 1:
            self.setPlayerB(player_id)
        else:
            self.setPlayerA(player_id)
        return True

    async def setGameStarted(self):
        self.game_started = True
        name_list = []
        playera_name = "Unknown"
        playerb_name = "Unknown"
        playera_avatar = "img/149071.png"
        playerb_avatar = "img/149071.png"
        type_game = "0"
        try:
            url = 'http://authentification:8050/auth/user_info/'+self.getPlayerA()+","+self.getPlayerB()+"/"
            name_list = requests.get(url).json()
        except Exception as e:
            pass
        print(name_list)
        if self.getPlayerA() in name_list:
            playera_name = name_list[self.getPlayerA()]["username"]
            playera_avatar = name_list[self.getPlayerA()]["profile_picture"]
        
        if self.getPlayerB() in name_list:
            playerb_name = name_list[self.getPlayerB()]["username"]
            playerb_avatar = name_list[self.getPlayerB()]["profile_picture"]

        if self.game_ia == True:
            type_game = "1"

        obj = {
            "type": type_game,
            "player1_name": playera_name,
            "player2_name": playerb_name,
            "player1_avatar": playera_avatar,
            "player2_avatar": playerb_avatar
        }
        game_obj = self.getGameAsJSON()

        await RoomRequest.infoTreeGameSingle(room_client_manager.getClientById(self.getPlayerA()).getObj(), obj, "0")
        await RoomRequest.infoTreeGameSingle(room_client_manager.getClientById(self.getPlayerB()).getObj(), obj, "0")
        await game_manager.createGame(
            game_obj['match_id'],
            game_obj['player1_id'],
            game_obj['player2_id'],
            game_obj['tournament_id'],
            game_obj['time'])
        #post_request.addPostRoomMatch(self.getGameAsJSON())

    def setGameIa(self, ia):
        self.game_ia = ia

    def setAllPlayersInGameStatus(self, status):
        if self.getPlayerA() != "":
            room_client_manager.getClientById(self.getPlayerA()).setInGame(status)
        if self.getPlayerB() != "":
            room_client_manager.getClientById(self.getPlayerB()).setInGame(status)

    def leaveAllPlayers(self):
        if room_client_manager.isClientIdExist(self.player_id_a):
            room_client_manager.getClientById(self.player_id_a).setInARoom(False)
            room_client_manager.getClientById(self.player_id_a).setInGame(False)

        if room_client_manager.isClientIdExist(self.player_id_b):
            room_client_manager.getClientById(self.player_id_b).setInARoom(False)
            room_client_manager.getClientById(self.player_id_b).setInGame(False)


    # ======= GETTER =======

    def getId(self):
        return self.id

    def getPlayerA(self):
        return self.player_id_a

    def getPlayerB(self):
        return self.player_id_b

    def getScorePlayerA(self):
        return self.score_player_a

    def getScorePlayerB(self):
        return self.score_player_b

    def getGameStartDate(self):
        return self.game_start_date

    def getGameEndedDate(self):
        return self.game_end_date

    def getCreatedDate(self):
        return self.created_date

    def getPlayerNb(self):
        if self.player_id_b != "" and self.player_id_b != "":
            return 2
        if self.player_id_a != "" or self.player_id_b != "":
            return 1
        return 0

    def getGameStartedDate(self):
        return self.game_started

    def getGameIa(self):
        return self.game_ia

    def getGameAsJSON(self):
        obj = {
            "match_id": self.id,
            "tournament_id": 0,
            "player1_id": self.getPlayerA(),
            "player2_id": self.getPlayerB(),
            "time": Uniqid.getUnixTimeStamp()
        }
        return obj

    def playerIdIsInRoom(self, player_id):
        if self.player_id_a == player_id or self.player_id_b == player_id:
            return True
        return False

    def isWaiting(self):
        if self.getGameIa() is False and self.getPlayerNb() == 1:
            return True
        return False
