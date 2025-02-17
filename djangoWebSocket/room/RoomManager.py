from room.Room import Room


class RoomManager:
    def __init__(self):
        self.rooms = []

    def createRoom(self):
        room = Room()
        self.rooms.append(room)
        return room.getId()

    def removeRoomById(self, roomId):
        if self.isRoomIdExist(roomId):
            self.getRoomById(roomId).leaveAllPlayers()

        initial_len = len(self.rooms)
        self.rooms = [room for room in self.rooms if room.getId() != roomId]
        if len(self.rooms) == initial_len:
            return False
        return True

    def getRooms(self):
        return self.rooms

    def isRoomIdExist(self, roomId):
        for room in self.rooms:
            if str(room.getId()) == str(roomId):
                return True
        return False

    def getRoomById(self, roomId):
        for room in self.rooms:
            if room.getId() == roomId:
                return room
        return False

    def getWaitingRoom(self):
        for room in self.rooms:
            if room.isWaiting():
                return room.getId()
        return False


room_manager = RoomManager()
