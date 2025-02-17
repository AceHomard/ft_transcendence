class ClientManager:
    def __init__(self):
        self.clients = []

    def addClient(self, client):
        self.clients.append(client)

    def removeClient(self, client_id):
        for client in self.clients:
            if client.getSessionId() == client_id:
                self.clients.remove(client)
                return True
        return False

    def getClients(self):
        return self.clients

    def isClientIdExist(self, sessionId):
        for client in self.clients:
            if client.getSessionId() == sessionId:
                return True
        return False

    def getClientById(self, sessionId):
        for client in self.clients:
            if client.getSessionId() == sessionId:
                return client
        return False


client_manager = ClientManager()
