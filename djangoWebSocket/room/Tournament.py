from api.PostRequest import post_request
from room.Room import Room
from room.RoomRequest import RoomRequest
from room.RoomClientManager import room_client_manager
import requests
import uuid
import time
from room.UniqId import Uniqid
from .loger_config import setup_logger
from game.GameManager import game_manager
from sty import fg, bg, ef, rs

logger = setup_logger(__name__)

class Tournament:
    id = 0
    created_date = 0
    demi_room_a = None
    demi_room_b = None
    final_room = None
    demi_room_a_result = {}
    demi_room_b_result = {}
    final_room_result = {}
    players = []
    status = 0  # 0: waiting | 1: tournament start | 2: end of one demi game | 3: end of all demi game | 4: tour finish

    def __init__(self):
        self.id = Uniqid.generate()
        self.created_date = Uniqid.getUnixTimeStamp()

        self.demi_room_a = Room()
        self.demi_room_b = Room()
        self.final_room = Room()

        self.players = []
        self.demi_room_a_result = []
        self.demi_room_b_result = []
        self.final_room_result = []
        self.status = 0
        pass

    async def __upStatus(self):
        self.status += 1
        print("status:", self.status)
        if self.status == 1:
            await self.sendTree()

            game_a_obj = self.demi_room_a.getGameAsJSON()
            game_b_obj = self.demi_room_b.getGameAsJSON()

            await game_manager.createGame(
                game_a_obj['match_id'],
                game_a_obj['player1_id'],
                game_a_obj['player2_id'],
                self.getId(),
                game_a_obj['time'])

            await game_manager.createGame(
                game_b_obj['match_id'],
                game_b_obj['player1_id'],
                game_b_obj['player2_id'],
                self.getId(),
                game_b_obj['time'])
            return
        if self.status == 2:
            logger.info(fg.blue + str(self.id)+"[GAME ENGINE] 1er demi match fini"+ fg.white)
            try:
                player_a = self.final_room.getPlayerA()
                if room_client_manager.isClientIdExist(player_a):
                    player_act = room_client_manager.getClientById(player_a)
                    player_act.setFinalWaiting(True)
                    await RoomRequest.tourFinalWaiting(player_act.getObj())
            except Exception as e:
                print(fg.red + str(e))
        if self.status == 3:
            logger.info(str(self.id)+"[GAME ENGINE] 2eme demi match fini"+ fg.white)
            await self.sendTree()
            player_a = self.final_room.getPlayerA()
            if room_client_manager.isClientIdExist(player_a):
                room_client_manager.getClientById(player_a).setFinalWaiting(False)
            #post_request.addPostRoomMatch(self.final_room.getGameAsJSON())
            print("final_room start")
            game_obj = self.final_room.getGameAsJSON()

            await game_manager.createGame(
                game_obj['match_id'],
                game_obj['player1_id'],
                game_obj['player2_id'],
                self.getId(),
                game_obj['time'])
        if self.status == 4:
            logger.info(str(self.id)+"[GAME ENGINE] match fini")
            all_match = [self.demi_room_a_result, self.demi_room_b_result, self.final_room_result]
            print(all_match)
            post_request.addPostResultTour(all_match)
        


    async def startTournament(self):
        self.demi_room_a.addPlayer(self.players[0])
        self.demi_room_a.addPlayer(self.players[1])
        self.demi_room_b.addPlayer(self.players[2])
        self.demi_room_b.addPlayer(self.players[3])
        await self.__upStatus()
        self.setAllPlayersInGameStatus(True)
        
    # ======= SETTER =======

    async def sendTree(self):
        name_list = []
        player_name = ["Unknown", "Unknown", "Unknown", "Unknown"]
        player_avatar = ["img/149071.png", "img/149071.png", "img/149071.png", "img/149071.png"]
        player_win = ["0", "0", "0", "0"]
        name_str = self.players[0]+","+self.players[1]+","+self.players[2]+","+self.players[3]

        try:
            url = 'http://authentification:8050/auth/user_info/'+name_str+"/"
            name_list = requests.get(url).json()
        except Exception as e:
            pass

        if self.players[0] in name_list:
            player_name[0] = name_list[self.players[0]]["username"]
            player_avatar[0] = name_list[self.players[0]]["profile_picture"]
        if self.players[1] in name_list:
            player_name[1] = name_list[self.players[1]]["username"]
            player_avatar[1] = name_list[self.players[1]]["profile_picture"]
        if self.players[2] in name_list:
            player_name[2] = name_list[self.players[2]]["username"]
            player_avatar[2] = name_list[self.players[2]]["profile_picture"]
        if self.players[3] in name_list:
            player_name[3] = name_list[self.players[3]]["username"]
            player_avatar[3] = name_list[self.players[3]]["profile_picture"]

        final_player_a_name = "?"
        final_player_a_avatar = "img/149071.png"
        final_player_b_name = "?"
        final_player_b_avatar = "img/149071.png"
        
        final_unknown = "1"
        if self.status >= 3:
            final_unknown = "0"
            id_a = self.final_room.getPlayerA()
            id_b = self.final_room.getPlayerB()
            player_win = ["2", "2", "2", "2"]
            if self.demi_room_a.getPlayerA() == id_a or self.demi_room_a.getPlayerA() == id_b:
                player_win[0] = "0"
            else:
                player_win[1] = "0"
            if self.demi_room_b.getPlayerA() == id_a or self.demi_room_b.getPlayerA() == id_b:
                player_win[2] = "0"
            else:
                player_win[3] = "0"
            if id_a in name_list:
                final_player_a_name = name_list[id_a]["username"]
                final_player_a_avatar = name_list[id_a]["profile_picture"]
            if id_b in name_list:
                final_player_b_name = name_list[id_b]["username"]
                final_player_b_avatar = name_list[id_b]["profile_picture"]

        obj = {
            "left_game": [
                {"name": player_name[0], "avatar": player_avatar[0], "win": player_win[0]},
                {"name": player_name[1], "avatar": player_avatar[1], "win": player_win[1]}
            ],
            "right_game": [
                {"name": player_name[2], "avatar": player_avatar[2], "win": player_win[2]},
                {"name": player_name[3], "avatar": player_avatar[3], "win": player_win[3]}
            ],
            "final_game": [
                {"name": final_player_a_name, "avatar": final_player_a_avatar, "unknown": final_unknown},
                {"name": final_player_b_name, "avatar": final_player_b_avatar, "unknown": final_unknown}
            ]
        }

        await RoomRequest.infoTreeGame(self.id, obj, "1")

    def addPlayer(self, player_id):
        if self.getPlayerNb() < 4:
            self.players.append(player_id)
            return True
        return False

    def removePlayer(self, player_id):
        if self.status != 0:
            return False
        if self.playerIsInTournament(player_id):
            self.players.remove(player_id)
            return True
        return False

    def setAllPlayersInGameStatus(self, status):
        for player in self.players:
            room_client_manager.getClientById(player).setInGameTour(status)

    def leaveAllPlayers(self):
        for player in self.players:
            if room_client_manager.isClientIdExist(player):
                room_client_manager.getClientById(player).setInARoomTour(False)
                room_client_manager.getClientById(player).setInGameTour(False)
                room_client_manager.getClientById(player).setInARoom(False)
                room_client_manager.getClientById(player).setInGame(False)

    async def leaveSpecificPlayer(self, id_player):
        #remove player from list 
        #if id_player in self.players:
        #    self.players.remove(id_player)
        #    self.players.append(id_player+"_deco")
        
        if room_client_manager.isClientIdExist(id_player):
            player = room_client_manager.getClientById(id_player)
            await player.removeChannel(player.getObj(), self.id)
            player.setInARoomTour(False)
            player.setInGameTour(False)
            player.setInARoom(False)
            player.setInGame(False)

    # ======= GETTER =======

    def getId(self):
        return self.id

    def getCreatedDate(self):
        return self.created_date

    def getPlayerNb(self):
        return len(self.players)

    def getDemiRoomA(self):
        return self.demi_room_a

    def getDemiRoomB(self):
        return self.demi_room_b

    def getFinalRoom(self):
        return self.final_room

    def playerIsInTournament(self, player_id):
        if player_id in self.players:
            return True
        return False

    def isWaiting(self):
        if self.getPlayerNb() != 4:
            return True
        return False

    def isRoomExistsById(self, room_id):
        if self.final_room.getId() == room_id:
            return True
        if self.demi_room_a.getId() == room_id:
            return True
        if self.demi_room_b.getId() == room_id:
            return True
        return False

    async def setRoomResult(self, room_id, result):
        print("setRoomResult")
        try:
            if self.demi_room_a.getId() == room_id:
                self.demi_room_a_result = result
                self.final_room.addPlayer(result["winner_id"])
                print(fg.blue + self.demi_room_a.getPlayerA(), self.demi_room_a.getPlayerB()+ fg.white)
                if self.demi_room_a.getPlayerA() == result["winner_id"]:
                    await self.leaveSpecificPlayer(self.demi_room_a.getPlayerB())
                else:
                    await self.leaveSpecificPlayer(self.demi_room_a.getPlayerA())
            if self.demi_room_b.getId() == room_id:
                self.demi_room_b_result = result
                self.final_room.addPlayer(result["winner_id"])
                print(fg.blue + self.demi_room_b.getPlayerA(), self.demi_room_b.getPlayerB()+ fg.white)
                if self.demi_room_b.getPlayerA() == result["winner_id"]:
                    await self.leaveSpecificPlayer(self.demi_room_b.getPlayerB())
                else:
                    await self.leaveSpecificPlayer(self.demi_room_b.getPlayerA())
            if self.final_room.getId() == room_id:
                self.final_room_result = result
                await self.leaveSpecificPlayer(self.final_room.getPlayerA())
                await self.leaveSpecificPlayer(self.final_room.getPlayerB())
        except Exception as e:
                print(fg.red + str(e)+ fg.white)
    
    async def setRoomResultUpdate(self, room_id):
        print("setRoomResultUpdate")
        if self.demi_room_a.getId() == room_id:
            await self.__upStatus()
        if self.demi_room_b.getId() == room_id:
            await self.__upStatus()
        if self.final_room.getId() == room_id:
            await self.__upStatus()
