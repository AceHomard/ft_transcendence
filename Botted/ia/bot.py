import json
import websocket
import threading
import time

SCREEN_HEIGHT = 320
SCREEN_WIDTH = 650
BOT_HEIGHT = 100

class Bot:

    Bot_position_y = SCREEN_HEIGHT / 2 - BOT_HEIGHT / 2
    current_time = time.time()
    previson = Bot_position_y
    

    def __init__(self, player_id):
        self.player_id = player_id
        self.ws = None

    def printDATA(self, msg):
        print("\33[31m" + str(self.player_id) + ": \33[37m" + str(msg))

    def run(self):
        self.connect()

    def connect(self):
        self.ws = websocket.WebSocketApp("ws://matchmaking:8065/ws/game/",
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.run_forever()

    def on_message(self, ws, message):
        data = json.loads(message)
        #self.printDATA(data)
        time_passed = time.time() - self.current_time
        if (time_passed >= 1 and data.get('action') == 'movement_ball'):
            self.current_time = time.time()
            self.algo(data)
        elif(data.get('action') == 'score_game'):
            print('reset bot')
            self.Bot_position_y = SCREEN_HEIGHT / 2 - BOT_HEIGHT / 2
            self.prevision = SCREEN_HEIGHT / 2 - BOT_HEIGHT / 2
        if data.get('type') == 'connection_etalished':
            self.authenticate(ws)

    def authenticate(self, ws):
        self.printDATA("Auth: "+str(self.player_id))
        ws.send(json.dumps({
            "action": "auth",
            "session_id": self.player_id,
            "player_id": self.player_id
        }))

    def on_error(self, ws, error):
        self.printDATA("Error:" + str(error))

    def on_close(self, ws, close_status_code, close_msg):
        self.printDATA("### closed ###")

    def on_open(self, ws):
        #printDATA("Opened connection")
        self.authenticate(ws)

    def close_connection(self):
        if self.ws:
            self.ws.close()
            self.printDATA("Connection closed.")
        else:
            self.printDATA("No active connection to close.")

    def reopen_connection(self):
        self.printDATA("Reopening connection...")
        self.connect()

    def algo(self, data):
        ball_x = data.get('ball_x') 
        ball_y = data.get('ball_y')
        ball_speed = data.get('ball_speed')
        self.prevision = self.prediction(ball_y, ball_x, ball_speed)
        if (self.prevision > self.Bot_position_y + BOT_HEIGHT / 2):
            while(self.Bot_position_y + BOT_HEIGHT / 2 < self.prevision):
                time.sleep((0.017))
                if (self.Bot_position_y + BOT_HEIGHT + 4 >= SCREEN_HEIGHT):
                    print('stop parce que trop bas')
                    break
                message = json.dumps({'action': 'move_paddle', 'mouvement': 4, 'player_id': 'bot'})
                self.ws.send(message)
                self.Bot_position_y += 4
        elif (self.prevision < self.Bot_position_y + BOT_HEIGHT / 2):
            while(self.Bot_position_y + BOT_HEIGHT / 2 > self.prevision):
                time.sleep((0.017))
                if (self.Bot_position_y - 4 <= 0):
                    break
                message = json.dumps({'action': 'move_paddle', 'mouvement': -4, 'player_id': 'bot'})
                self.ws.send(message)
                self.Bot_position_y -= 4

    def prediction(self, ball_y, ball_x, ball_speed):
            prevision_deepness = self.movement_before_vertical_wall(ball_x, ball_speed)
            if (prevision_deepness > 60):
                prevision_deepness = 60
            futur_position = ball_y + (ball_speed['y'] * prevision_deepness)
            return self.correct_prediction_y(futur_position)
    
    def correct_prediction_y(self, prediciton):
        if prediciton > SCREEN_HEIGHT:
            prediciton = SCREEN_HEIGHT - (prediciton - SCREEN_HEIGHT)
        elif prediciton < 0:
            prediciton = prediciton * -1
        return (prediciton)
    
    def movement_before_vertical_wall(self, ball_x, ball_speed):
        if (ball_speed['x'] > 0):
            movement_left = (SCREEN_WIDTH - ball_x) / 4
        else:
            movement_left = ball_x / 4
        return (movement_left)
 
class BotManager:

    def __init__(self):
        self.clients = {}
        self.threads = {}

    def addBot(self, bot_id):
        self.clients[bot_id] = Bot(bot_id)
        thread = threading.Thread(target=self.clients[bot_id].run)
        self.threads[bot_id] = thread
        self.threads[bot_id].start()