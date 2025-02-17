from language.Language import language
from notification.Request import Request


class Client:
    session_id = ""
    player_id = ""
    lang = ""
    channels = []
    obj = None

    def __init__(self, obj):
        self.obj = obj
        self.session_id = ""
        self.player_id = ""
        self.lang = "fr"
        self.channels = []

    # ======= SETTER =======
    def setSessionId(self, session_id):
        self.session_id = session_id

    def setPlayerId(self, player_id):
        self.player_id = player_id

    def setLang(self, lang):
        self.lang = lang

    async def addChannel(self, obj, channel):
        self.channels.append(channel)
        await obj.channel_layer.group_add(channel, obj.channel_name)

    async def removeChannel(self, obj, channel):
        self.channels.remove(channel)
        await obj.channel_layer.group_discard(channel, obj.channel_name)

    async def leaveChannel(self, obj, channel):
        await obj.channel_layer.group_discard(channel, obj.channel_name)

    async def notification(self, status, title, message):
        lang = self.getLang()
        await Request.notification(self.obj, status,
                    language.get(lang, title),
                    language.get(lang, message))

    # ======= GETTER =======

    def getSessionId(self):
        return self.session_id

    def getPlayerId(self):
        return self.player_id

    def getLang(self):
        return self.lang

    def getChannels(self):
        return self.channels


