import time, asyncio
import random

from game.ClientManager import client_manager
from room.RoomClientManager import room_client_manager
from game.ConsumerRequest import ConsumerRequest
from api.PostRequest import post_request
from game.Cooldown import Cooldown
from room.UniqId import Uniqid
from game.Player import Player
from game.objects import Ball
import threading
import requests
from .loger_config import setup_logger

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 320
PLAYER_HEIGHT = 100
PLAYER_WIDTH = 5
logger = setup_logger(__name__)

class Game:
    id = ""
    player_a = None
    player_b = None
    ball = None
    player_a_connected = False
    player_b_connected = False
    game_start = False
    game_ended = False
    tournament_id = False
    time_waiting = 0
    max_score = 0
    cooldown = False

    def __init__(self, game_id, player_a_id, player_b_id, tournament_id, time_waiting):
        self.last_refresh_time = time.time()
        self.id = game_id
        self.player_a = Player(id=player_a_id, x=0, y=SCREEN_HEIGHT / 2 - PLAYER_HEIGHT / 2, score=0)
        self.player_b = Player(id=player_b_id, x=SCREEN_WIDTH - PLAYER_WIDTH, y=SCREEN_HEIGHT / 2 - PLAYER_HEIGHT / 2, score=0)
        self.ball = Ball(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2, r=5, speed={'x': 0, 'y': 0})
        self.setRandomStartBallSpeed()
        self.player_a_connected = False
        self.player_b_connected = False
        self.game_start = False
        self.game_ended = False
        self.tournament_id = tournament_id
        self.time_waiting = time_waiting
        self.max_score = 3
        self.cooldown = False

    async def connectPlayerA(self):
        print("connectPlayerA", self.getPlayerAId())
        if client_manager.isClientIdExist(self.getPlayerAId()):
            player = client_manager.getClientById(self.getPlayerAId())
            self.player_a_connected = True
            await player.addChannel(player.obj, self.id+"_game")

    async def connectPlayerB(self):
        print("connectPlayerB", self.getPlayerBId())
        if client_manager.isClientIdExist(self.getPlayerBId()):
            player = client_manager.getClientById(self.getPlayerBId())
            self.player_b_connected = True
            await player.addChannel(player.obj, self.id+"_game")

    async def timerWaiting(self):
        if self.cooldown.getCooldown(3000, 1, 2) == 1:
            await self.GameSideSend()
            await ConsumerRequest.infoTimeGame(self.id+"_game", "3")

        if self.cooldown.getCooldown(1000, 2, 3) == 1:
            await ConsumerRequest.infoTimeGame(self.id+"_game", "2")
            
        if self.cooldown.getCooldown(1000, 3, 4) == 1:
            await ConsumerRequest.infoTimeGame(self.id+"_game", "1")
            
        if self.cooldown.getCooldown(1000, 4, 5) == 1:
            await ConsumerRequest.infoTimeGame(self.id+"_game", "GO")
            await self.gameStarter()
            logger.info(str(self.id)+"[GAME ENGINE] GO END TIMER")

    async def GameSideSend(self):
        try:
            name_list = []
            playera_name = "Unknown"
            playerb_name = "Unknown"
            playera_avatar = "img/149071.png"
            playerb_avatar = "img/149071.png"
            type_game = "0"
            try:
                url = 'http://authentification:8050/auth/user_info/'+self.getPlayerAId()+","+self.getPlayerBId()+"/"
                name_list = requests.get(url).json()
            except Exception as e:
                print(e)
                pass

            if self.getPlayerAId() in name_list:
                playera_name = name_list[self.getPlayerAId()]["username"]
                playera_avatar = name_list[self.getPlayerAId()]["profile_picture"]
            
            if self.getPlayerBId() in name_list:
                playerb_name = name_list[self.getPlayerBId()]["username"]
                playerb_avatar = name_list[self.getPlayerBId()]["profile_picture"]

            obj = {
                "player1_name": playera_name,
                "player2_name": playerb_name,
                "player1_avatar": playera_avatar,
                "player2_avatar": playerb_avatar
            }
            await ConsumerRequest.GameSide(self.id+"_game", obj)
        except Exception as e:
            print(e)
            pass


    async def gameStarter(self):
        await ConsumerRequest.startGame(self.id+"_game")
        await ConsumerRequest.playerSide(client_manager.getClientById(self.getPlayerAId()).obj, "left")
        await ConsumerRequest.playerSide(client_manager.getClientById(self.getPlayerBId()).obj, "right")
        self.game_start = True
        self.last_refresh_time = time.time()
        logger.info(str(self.id)+"[GAME ENGINE] GAME STARTED")

    async def gameStart(self):
        self.cooldown = Cooldown(int(time.time() * 1000), 1)
        self.update_task = asyncio.create_task(self.game_loop())
  
    def getPlayerAScore(self):
        return (self.player_a.score)
    
    def getPlayerBScore(self):
        return (self.player_b.score)
    
    def winnerPlayer(self):
        if (self.getPlayerAScore() == self.max_score):
            return self.getPlayerAId()
        return self.getPlayerBId()

    def getGameAsJSON(self):
        obj = {
            "match_id": self.id,
            "tournament_id": self.tournament_id,
            "player1_id": self.getPlayerAId(),
            "player2_id": self.getPlayerBId(),
            "player1_score": self.getPlayerAScore(),
            "player2_score": self.getPlayerBScore(),
            "winner_id": self.winnerPlayer(),
        }
        return obj

    async def gameEndResultTour(self):
        if self.cooldown.getCooldown(5000, 6, 7) == 1:
            from room.TournamentManager import tournament_manager

            try:
                game_data = self.getGameAsJSON()
                self.update_task.cancel()

                if not tournament_manager.isTournamentIdExist(str(game_data["tournament_id"])):
                    return

                tour = tournament_manager.getTournamentById(str(game_data["tournament_id"]))
                if not tour.isRoomExistsById(str(game_data["match_id"])):
                    return

                await tour.setRoomResultUpdate(self.id)
                if tour.status == 4:
                    tournament_manager.removeTournamentById(str(game_data["tournament_id"]))

            except Exception as e:
                print(e)

    async def gameEnd(self, winner_id):
        winner = "Unknown"
        name_list = []
        try:
            url = 'http://authentification:8050/auth/user_info/'+winner_id+"/"
            name_list = requests.get(url).json()
        except Exception as e:
            pass
        if winner_id in name_list:
            winner = name_list[winner_id]["username"]

        await ConsumerRequest.endGame(self.id+"_game", winner)
        self.game_ended = True
        await self.endGameRequest(self.getGameAsJSON())

        self.game_start = False
        logger.info(str(self.id)+"[GAME ENGINE] GAME FINISHED")

    def isReady(self):
        if self.player_a_connected and self.player_b_connected:
            return True
        return False

    def getPlayerAId(self):
        return self.player_a.id

    def getPlayerBId(self):
        return self.player_b.id

    def playerIsInGame(self, player_id):
        if player_id == self.getPlayerAId() or player_id == self.getPlayerBId():
            return True
        return False

    async def leaveChannelById(self, player_id):
        if client_manager.isClientIdExist(player_id):
            player_id = client_manager.getClientById(player_id)
            await player_id.removeChannel(player_id.obj, self.id+"_game")

    async def endGameRequest(self, game_data):
        from room.RoomManager import room_manager
        from room.TournamentManager import tournament_manager

        if game_data["tournament_id"] == 0:
            try:
                if not room_manager.isRoomIdExist(str(game_data["match_id"])):
                    return
                game_data["timestamp"] = Uniqid.getUnixTimeStamp()
                    
                await self.leaveChannelById(self.getPlayerAId())
                await self.leaveChannelById(self.getPlayerBId())
                
                self.update_task.cancel()
                #FOR DEBUG
                if room_manager.getRoomById(str(game_data["match_id"])).game_ia == False:
                    post_request.addPostResultMatch(game_data)
                else:
                    print("IA GAME")
                room_manager.removeRoomById(str(game_data["match_id"]))
                return
            except Exception as e:
                print(e)
        else:
            try:
                if not tournament_manager.isTournamentIdExist(str(game_data["tournament_id"])):
                    return

                tour = tournament_manager.getTournamentById(str(game_data["tournament_id"]))
                if not tour.isRoomExistsById(str(game_data["match_id"])):
                    return

                await self.leaveChannelById(self.getPlayerAId())
                await self.leaveChannelById(self.getPlayerBId())
                room_manager.removeRoomById(str(game_data["match_id"]))

                game_data["timestamp"] = Uniqid.getUnixTimeStamp()
                await tour.setRoomResult(str(game_data["match_id"]), game_data)

                self.cooldown.setCooldown(int(time.time() * 1000), 6)
                
            except Exception as e:
                print(e)

    # ===== GAME ENGINE =====

    async def game_loop(self):
        while True:
            current_time = time.time()
            time_elapsed = current_time - self.last_refresh_time
            self.last_refresh_time = current_time
            if self.game_start:
                await self.update_ball_position(time_elapsed)
                await ConsumerRequest.playerMove(self.id+"_game", self.player_b.y, self.player_b.id)
                await ConsumerRequest.playerMove(self.id+"_game", self.player_a.y, self.player_a.id)
            else:
                await self.timerWaiting()
            await self.gameEndResultTour()
            await asyncio.sleep(0.05)

    async def syncGameState(self, player_id):
        if not self.game_start:
            return
        if player_id == self.getPlayerAId():
            await ConsumerRequest.playerSide(client_manager.getClientById(self.getPlayerAId()).obj, "left")
        else:
            await ConsumerRequest.playerSide(client_manager.getClientById(self.getPlayerBId()).obj, "right")
        await self.sendGameState()

    async def sendGameState(self):
        await ConsumerRequest.scoreGame(self.id+"_game", self.player_a.score, self.player_b.score)
        await ConsumerRequest.ballMove(self.id+"_game", self.ball)
        await ConsumerRequest.playerMove(self.id+"_game", self.player_a.y, self.getPlayerAId())
        await ConsumerRequest.playerMove(self.id+"_game", self.player_b.y, self.getPlayerBId())

    async def centerPose(self):
        ball = self.ball
        ball.x = SCREEN_WIDTH / 2
        ball.y = SCREEN_HEIGHT / 2
        self.setRandomStartBallSpeed()
        self.player_a.y = SCREEN_HEIGHT / 2 - PLAYER_HEIGHT / 2
        self.player_b.y = SCREEN_HEIGHT / 2 - PLAYER_HEIGHT / 2
        await self.sendGameState()

    async def checkScoreGame(self):
        if self.player_a.score >= self.max_score:
            await self.gameEnd(self.getPlayerAId())
        if self.player_b.score >= self.max_score:
            await self.gameEnd(self.getPlayerBId())

    def BounceEffect(self, player):
        ball = self.ball
        impact = ball.y - player.y - PLAYER_HEIGHT / 2
        ratio = 1.5
        ball.speed['y'] = round(impact * ratio / 10)
        if (ball.speed['y'] == 0):
            ball.speed['y'] = 1

    def ballBounce(self):
        ball = self.ball
        if ball.speed['x'] * -1.2 > 15:
            ball.speed['x'] = 15
        elif ball.speed['x'] * -1.2 < -15:
            ball.speed['x'] = -15
        else:
            ball.speed['x'] *= -1.2

    def setRandomStartBallSpeed(self):
        ball = self.ball
        if random.choice([True, False]):
            ball.speed['x'] = random.uniform(3, 5)
        else:
            ball.speed['x'] = random.uniform(-5, -3)
        ball.speed['y'] = random.uniform(-2, 2)
        print("[BALL] Start velocity:", abs(ball.speed['x'] + ball.speed['y']))

    async def update_ball_position(self, time_elapsed):
        ball = self.ball
        displacement_x = ball.speed['x'] * time_elapsed * 60
        displacement_y = ball.speed['y'] * time_elapsed * 60
        ball.x += displacement_x
        ball.y += displacement_y

        if ball.y < 0:
            ball.y = -ball.y
            ball.speed['y'] = -ball.speed['y']
        elif ball.y > SCREEN_HEIGHT:
            ball.y = SCREEN_HEIGHT - (ball.y - SCREEN_HEIGHT)
            ball.speed['y'] = -ball.speed['y']

        if ball.x + ball.r >= SCREEN_WIDTH - PLAYER_WIDTH:
            if (ball.y < self.player_b.y and ball.y + 5 < self.player_b.y) or (ball.y > self.player_b.y + PLAYER_HEIGHT and ball.y - 5 > self.player_b.y + PLAYER_HEIGHT):
                self.player_a.score += 1
                await self.centerPose()
                await self.checkScoreGame()
                return
            else:
                self.ballBounce()
                self.BounceEffect(self.player_b)

        if ball.x - ball.r <= PLAYER_WIDTH:
            if (ball.y < self.player_a.y and ball.y + 5 < self.player_a.y) or (ball.y > self.player_a.y + PLAYER_HEIGHT and ball.y - 5 > self.player_a.y + PLAYER_HEIGHT):
                self.player_b.score += 1
                await self.centerPose()
                await self.checkScoreGame()
                return
            else:
                self.ballBounce()
                self.BounceEffect(self.player_a)
        await ConsumerRequest.ballMove(self.id+"_game", self.ball)

    def move_api_paddle(self, player_id, mouvement):
        if not self.game_start:
            return
        if player_id == self.getPlayerAId():
            self.player_a.y += mouvement
            if self.player_a.y + 100 > SCREEN_HEIGHT:
                self.player_a.y = SCREEN_HEIGHT - PLAYER_HEIGHT
            elif self.player_a.y < 0:
                self.player_a.y = 0
        if player_id == self.getPlayerBId():
            self.player_b.y += mouvement
            if self.player_b.y + 100 > SCREEN_HEIGHT:
                self.player_b.y = SCREEN_HEIGHT - PLAYER_HEIGHT
            elif self.player_b.y < 0:
                self.player_b.y = 0

    async def move_paddle(self, player_id, mouvement):
        if not self.game_start:
            return
        if player_id == self.getPlayerAId() and (self.player_a.y + mouvement <= SCREEN_HEIGHT and self.player_a.y + mouvement >= 0):
            self.player_a.y += mouvement
            await ConsumerRequest.playerMove(self.id+"_game", self.player_a.y, player_id)
        if player_id == self.getPlayerBId() and (self.player_b.y + mouvement <= SCREEN_HEIGHT and self.player_b.y + mouvement >= 0):
            self.player_b.y += mouvement
            if self.player_b.y + PLAYER_HEIGHT > SCREEN_HEIGHT:
                self.player_b.y = SCREEN_HEIGHT - PLAYER_HEIGHT
            elif self.player_b.y < 0:
                self.player_b.y = 0
            await ConsumerRequest.playerMove(self.id+"_game", self.player_b.y, player_id)
