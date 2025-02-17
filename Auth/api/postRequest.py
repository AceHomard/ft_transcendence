import json
import time

import requests

from .Signature import Signature
from threading import Thread

NOTIF_URL = "http://notification"
NOTIF_HOST = "8067"


class PostRequest:
    def __init__(self):
        self.posts_notif = []
        thread = Thread(target=self.retryLoop)
        thread.daemon = True
        thread.start()

    def addPostNotif(self, post):
        if post not in self.posts_notif:
            self.posts_notif.append(post)

    def removePostNotif(self, post):
        if post in self.posts_notif:
            self.posts_notif.remove(post)

    def tryPosts(self):
        for post in self.posts_notif:
            self.pushNotif(post)

    def retryLoop(self):
        while True:
            self.tryPosts()
            time.sleep(5)

    # =========== SEND ===========

    def pushNotif(self, notif):
        try:
            data, signature, headers = Signature.create_signed_token(notif, "api/keyauthapi/notification/private_key.pem")

            host = NOTIF_URL + ":" + NOTIF_HOST
            url = host + '/push_notif/'
            x = requests.post(url, json=data, headers=headers)
            self.removePostNotif(notif)
        except Exception as e:
            pass


post_request = PostRequest()
