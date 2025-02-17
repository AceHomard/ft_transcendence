class ClientManager:
    def __init__(self):
        self.clients = []

    def addClient(self, client):
        self.clients.append(client)

    def getClients(self):
        return self.clients

    def isClientIdExist(self, playerId):
        for client in self.clients:
            if client.getPlayerId() == playerId:
                return True
        return False

    def getClientById(self, playerId):
        for client in self.clients:
            if client.getPlayerId() == playerId:
                return client
        return False

    def printAll(self):
        print("Variables de RoomClientManager :")
        for a in self.clients:
            print("- "+str(a.getSessionId()))


client_manager = ClientManager()
