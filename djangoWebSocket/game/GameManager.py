from game.Game import Game


class GameManager:
    games = []

    def __init__(self):
        pass

    async def createGame(self, game_id, player_a_id, player_b_id, tournament_id, time):
        if self.ifGameExist(game_id):
            return False
        game = Game(game_id, player_a_id, player_b_id, tournament_id, time)
        await game.connectPlayerA()
        await game.connectPlayerB()
        if game.isReady():
            await game.gameStart()
        self.games.append(game)
        return game

    def removeGameById(self, gameId):
        initial_len = len(self.games)
        self.games = [game for game in self.games if game.id != gameId]
        if len(self.games) == initial_len:
            return False
        return True


    def getAllGames(self):
        return self.games

    def ifGameExist(self, game_id):
        for game in self.games:
            if game.id == game_id:
                return True
        return False

    def getGameById(self, game_id):
        for game in self.games:
            if game.id == game_id:
                return game
        return False

    def clientIsInGame(self, player_id):
        games = game_manager.getAllGames()
        for game in games:
            if game.game_ended == False:
                if game.getPlayerAId() == player_id:
                    return True
                elif game.getPlayerBId() == player_id:
                    return True
        return False


    def getClientInGame(self, player_id):
        games = game_manager.getAllGames()
        for game in games:
            if game.game_ended == False:
                if game.getPlayerAId() == player_id:
                    return game.id
                elif game.getPlayerBId() == player_id:
                    return game.id
        return False


game_manager = GameManager()
