from room.RoomClientManager import room_client_manager
from api.PostRequest import post_request
from room.RoomRequest import RoomRequest
import requests
import json
import os


def readJson():
    file = "social_data/friends.json"
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, 'w') as f:
            json.dump({}, f, indent=4)
        return {}


def getByKey(key):
    createJsonKey(key)
    data = readJson()
    if key in data:
        return data[key]


def writeJson(data):
    file = "social_data/friends.json"
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)


def addToJsonArray(key, element):
    createJsonKey(key)
    data = readJson()
    if key in data:
        if element not in data[key]:
            data[key].append(element)
    else:
        data[key] = [element]
    writeJson(data)


def removeFromJsonArray(key, element):
    createJsonKey(key)
    data = readJson()
    if key in data and element in data[key]:
        data[key].remove(element)
    writeJson(data)


def createJsonKey(key):
    data = readJson()
    if key not in data:
        data[key] = []
    writeJson(data)


def isKeyExist(key):
    file = "social_data/friends.json"
    try:
        with open(file, 'r') as f:
            data = json.load(f)
        return key in data
    except FileNotFoundError:
        return False

async def addFriend(user_id, target_id):
    user = room_client_manager.getClientById(user_id)
    addToJsonArray(user_id, target_id)
    name_list = []
    try:
        url = 'http://authentification:8050/auth/user_info/'+target_id+"/"
        name_list = requests.get(url).json()
    except Exception as e:
        pass
    status = True
    if room_client_manager.isClientIdExist(target_id):
        status = room_client_manager.getClientById(target_id).getActive()
    await RoomRequest.addFriend(user.getObj(), target_id, name_list[target_id]["username"], status)
    notif_id = room_client_manager.getClientById(user_id)
    post_request.pushNotif({"user_id":notif_id.getNotifId(),"status":"info","title":"notif.info.title","message":"notif.info.social_add_friend"})


async def removeFriend(user_id, target_id):
    user = room_client_manager.getClientById(user_id)
    removeFromJsonArray(user_id, target_id)
    name_list = []
    try:
        url = 'http://authentification:8050/auth/user_info/'+target_id+"/"
        name_list = requests.get(url).json()
    except Exception as e:
        pass
    status = True
    if room_client_manager.isClientIdExist(target_id):
        status = room_client_manager.getClientById(target_id).getActive()
    await RoomRequest.removeFriend(user.getObj(), target_id, name_list[target_id]["username"], status)
    notif_id = room_client_manager.getClientById(user_id)
    post_request.pushNotif({"user_id":notif_id.getNotifId(),"status":"info","title":"notif.info.title","message":"notif.info.social_remove_friend"})


async def sendActualClientState(user_id, name_list):
    user = room_client_manager.getClientById(user_id)
    friends_list = getByKey(user_id)

    for client in room_client_manager.getClients():
        if user_id == client.getPlayerId() or client.getPlayerId() not in name_list or client.getActive() == False:
            continue
        if client.getPlayerId() in friends_list:
            friends_list.remove(client.getPlayerId())
            await RoomRequest.connectFriend(user.getObj(), client.getPlayerId(), name_list[client.getPlayerId()]["username"])
        else:
            await RoomRequest.connectOnline(user.getObj(), client.getPlayerId(), name_list[client.getPlayerId()]["username"])
    for friend in friends_list:
        await RoomRequest.connectFriend(user.getObj(), friend, name_list[friend]["username"])
        await RoomRequest.leaveFriend(user.getObj(), friend, name_list[friend]["username"])

async def joinClient(user_id):
    await RoomRequest.updateGlobalCount("room_lobby", room_client_manager.getLoggedClientsCount())

    name_list = []
    client_ids = [client.getPlayerId() for client in room_client_manager.getClients()]
    all_ids = set(getByKey(user_id) + client_ids)
    clients_string = ','.join(str(id_client) for id_client in all_ids)

    try:
        url = 'http://authentification:8050/auth/user_info/'+clients_string+"/"
        name_list = requests.get(url).json()
    except Exception as e:
        pass

    await sendActualClientState(user_id, name_list)
    for client in room_client_manager.getClients():
        if user_id == client.getPlayerId() or user_id not in name_list:
            continue
        if user_id in getByKey(client.getPlayerId()):
            await RoomRequest.connectFriend(client.getObj(), user_id, name_list[user_id]["username"])
            #friends connected
        else:
            await RoomRequest.connectOnline(client.getObj(), user_id, name_list[user_id]["username"])
            #online connected


async def leaveClient(user_id):
    if (user_id == ""):
        return
    await RoomRequest.updateGlobalCount("room_lobby", room_client_manager.getLoggedClientsCount())

    name_list = []
    clients_string = ','.join(str(client.getPlayerId()) for client in room_client_manager.getClients())

    try:
        url = 'http://authentification:8050/auth/user_info/'+clients_string+"/"
        name_list = requests.get(url).json()
    except Exception as e:
        pass

    user_info = name_list.get(user_id)
    if user_info and "username" in user_info:
        username = user_info["username"]
        for client in room_client_manager.getClients():
            if user_id == client.getPlayerId() or user_id not in name_list:
                pass
            if user_id in getByKey(client.getPlayerId()):
                await RoomRequest.leaveFriend(client.getObj(), user_id, username)
                #friends leave
            else:
                await RoomRequest.leaveOnline(client.getObj(), user_id, username)
                #online leave
