class Client:
    player_id = ""
    channels = []
    obj = None

    def __init__(self, obj):
        self. player_id = ""
        self.channels = []
        self.obj = obj

    # ======= SETTER =======

    def setPlayerId(self, player_id):
        self.player_id = player_id

    async def addChannel(self, obj, channel):
        self.channels.append(channel)
        await obj.channel_layer.group_add(channel, obj.channel_name)

    async def removeChannel(self, obj, channel):
        self.channels.remove(channel)
        await obj.channel_layer.group_discard(channel, obj.channel_name)

    async def leaveChannel(self, obj, channel):
        await obj.channel_layer.group_discard(channel, obj.channel_name)

    # ======= GETTER =======

    def getPlayerId(self):
        return self.player_id

    def getChannels(self):
        return self.channels

    # ======= OTHER =======

    def isAValidSession(self):
        if self.player_id != "":
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

