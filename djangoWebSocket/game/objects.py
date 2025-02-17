class Player:
    def __init__(self, id, x, y, score):
        self.id = id
        self.x = x
        self.y = y
        self.score = score


class Ball:
    def __init__(self, x, y, r, speed):
        self.x = x
        self.y = y
        self.r = r
        self.speed = speed


class Game:
    def __init__(self, player1, player2, ball):
        self.player1 = player1
        self.player2 = player2
        self.ball = ball