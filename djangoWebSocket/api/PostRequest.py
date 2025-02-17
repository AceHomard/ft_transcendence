import json
import time

import requests

from Log.Log import Log
from api.Signature import Signature
from api.urls_api import BLOCKCHAIN_URL, BLOCKCHAIN_HOST, GAMEENGINE_HOST, GAMEENGINE_URL, NOTIF_HOST, NOTIF_URL, BOT_HOST, BOT_URL
from threading import Thread


class PostRequest:
    def __init__(self):
        self.posts_result_match = []
        self.posts_result_tour = []
        self.posts_room_match = []
        self.posts_notif = []
        self.posts_bot = []
        thread = Thread(target=self.retryLoop)
        thread.daemon = True
        thread.start()

    def addPostResultMatch(self, post):
        if post not in self.posts_result_match:
            self.posts_result_match.append(post)

    def addPostResultTour(self, post):
        if post not in self.posts_result_tour:
            self.posts_result_tour.append(post)

    def addPostRoomMatch(self, post):
        if post not in self.posts_room_match:
            self.posts_room_match.append(post)

    def addPostNotif(self, post):
        if post not in self.posts_notif:
            self.posts_notif.append(post)

    def addPostBot(self, post):
        if post not in self.posts_bot:
            self.posts_bot.append(post)

    def removePostResultMatch(self, post):
        if post in self.posts_result_match:
            self.posts_result_match.remove(post)

    def removePostResultTour(self, post):
        if post in self.posts_result_tour:
            self.posts_result_tour.remove(post)

    def removePostRoomMatch(self, post):
        if post in self.posts_room_match:
            self.posts_room_match.remove(post)
    
    def removePostNotif(self, post):
        if post in self.posts_notif:
            self.posts_notif.remove(post)

    def removePostBot(self, post):
        if post in self.posts_bot:
            self.posts_bot.remove(post)

    def tryPosts(self):
        for post in self.posts_result_match:
            self.matchResult(post)
        for post in self.posts_result_tour:
            self.tourResult(post)
        #for post in self.posts_room_match:
        #    self.matchRoom(post)
        for post in list(self.posts_room_match):
            Thread(target=self.matchRoom, args=(post,)).start()
        for post in self.posts_notif:
            self.pushNotif(post)
        for post in self.posts_bot:
            self.pushBot(post)

    def retryLoop(self):
        while True:
            self.tryPosts()
            time.sleep(5)

    # =========== SEND ===========

    def matchResult(self, match):
        try:
            data, signature, headers = Signature.create_signed_token(match, "keydjangoWebSocketapi/blockchain/private_key.pem")

            host = BLOCKCHAIN_URL + ":" + BLOCKCHAIN_HOST
            url = host + '/match/post/'
            x = requests.post(url, json=data, headers=headers)
            Log.info("[API] Post 'matchResult'", x)
            self.removePostResultMatch(match)
        except Exception as e:
            Log.error("[API] Post 'matchResult' Error", e)

    def tourResult(self, tour):
        try:
            data, signature, headers = Signature.create_signed_token(tour, "keydjangoWebSocketapi/blockchain/private_key.pem")

            host = BLOCKCHAIN_URL + ":" + BLOCKCHAIN_HOST
            url = host + '/tournament/post/'
            x = requests.post(url, json=data, headers=headers)

            Log.info("[API] Post 'tourResult'", x)
            self.removePostResultTour(tour)
        except Exception as e:
            Log.error("[API] Post 'matchResult' Error", e)

    def matchRoom(self, match):
        try:
            data, signature, headers = Signature.create_signed_token(match, "keydjangoWebSocketapi/blockchain/private_key.pem")

            host = GAMEENGINE_URL + ":" + GAMEENGINE_HOST
            url = host + '/api/create_game/'
            x = requests.post(url, json=data, headers=headers)
            Log.info("[API] Post 'matchRoom'", x)
            self.removePostRoomMatch(match)
        except Exception as e:
            Log.error("[API] Post 'matchRoom' Error", e)

    def pushNotif(self, notif):
        try:
            data, signature, headers = Signature.create_signed_token(notif, "keydjangoWebSocketapi/notification/private_key.pem")

            host = NOTIF_URL + ":" + NOTIF_HOST
            url = host + '/push_notif/'
            x = requests.post(url, json=data, headers=headers)
            Log.info("[API] Post 'push_notif'", x)
            self.removePostNotif(notif)
        except Exception as e:
            Log.error("[API] Post 'push_notif' Error", e)

    def pushBot(self, bot):
        try:
            data, signature, headers = Signature.create_signed_token(bot, "keydjangoWebSocketapi/notification/private_key.pem")

            host = BOT_URL + ":" + BOT_HOST
            url = host + '/bot/create/'
            print(url)
            x = requests.post(url, json=data, headers=headers)
            Log.info("[API] Post 'push_bot'", x)
            self.removePostBot(bot)
        except Exception as e:
            Log.error("[API] Post 'push_bot' Error", e)

    # =========== GET ===========

    def APIvalidAuth(self, player_id):
        name_list = "{}"
        try:
            url = 'http://authentification:8050/auth/user_info/'+player_id+"/"
            response = requests.get(url)
            if response.status_code == 200:
                name_list = response.json()
        except Exception as e:
            pass

        return str(name_list) != "{}"


post_request = PostRequest()
