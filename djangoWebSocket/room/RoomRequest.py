import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class RoomRequest:

    @staticmethod
    async def connection(obj):
        await obj.send(
            text_data=json.dumps({
                "type": "connection_etalished",
                "message": "Room Connected"
                }))

    @staticmethod
    async def notification(obj, category, title, message):
        await obj.send(
            text_data=json.dumps({
                "type": "notification",
                "category": category,
                "title": title,
                "message": message
            }))

    @staticmethod
    async def waitingMatch(obj, status):
        await obj.send(
            text_data=json.dumps({
                "type": "waiting_match",
                "status": status
                }))

    @staticmethod
    async def foundMatch(room_group_name, match_id):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            room_group_name,
            {
                "type": "sendToGroup",
                "rq_type": "found_match",
                "match_id": match_id
            }
        )

    @staticmethod
    async def createRoom(room_group_name, room_id, ia_game, player_nb):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            room_group_name,
            {
                "type": "sendToGroup",
                "rq_type": "create_room",
                "room_id": room_id,
                "ia_game": ia_game,
                "player_nb": player_nb
            }
        )

    @staticmethod
    async def joinRoom(room_group_name, room_id, player_nb):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            room_group_name,
            {
                "type": "sendToGroup",
                "rq_type": "join_room",
                "room_id": room_id,
                "player_nb": player_nb
            }
        )

    @staticmethod
    async def waitingTour(room_group_name, status):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            room_group_name,
            {
                "type": "sendToGroup",
                "rq_type": "waiting_tour",
                "status": status
            }
        )

    @staticmethod
    async def waitingTime(obj, time):
        await obj.send(
            text_data=json.dumps({
                "type": "waiting_time",
                "waiting_time": time
                }))

    @staticmethod
    async def joinStatusTour(room_group_name, status, players):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            room_group_name,
            {
                "type": "sendToGroup",
                "rq_type": "join_status_tour",
                "status": status,
                "players": players
            }
        )

    @staticmethod
    async def joinStatusMatch(obj, status, players):
        await obj.send(
            text_data=json.dumps({
                "type": "join_status_match",
                "status": status,
                "players": players
            }))

    @staticmethod
    async def mmCanceled(obj):
        await obj.send(
            text_data=json.dumps({
                "type": "matchmaking_canceled",
            }))

    """
    SOCIAL:
    """
    @staticmethod
    async def updateGlobalCount(room_group_name, player_count):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            room_group_name,
            {
                "type": "sendToGroup",
                "rq_type": "social",
                "category": "update_global_count",
                "player_count": player_count
            }
        )

    @staticmethod
    async def connectFriend(obj, player_id, name):
        await obj.send(
            text_data=json.dumps({
                "type": "social",
                "category": "friends_connect",
                "player_id": player_id,
                "name": name,
                "status": True
            }))

    @staticmethod
    async def connectOnline(obj, player_id, name):
        await obj.send(
            text_data=json.dumps({
                "type": "social",
                "category": "online_connect",
                "player_id": player_id,
                "name": name,
                "status": True
            }))

    @staticmethod
    async def leaveFriend(obj, player_id, name):
        await obj.send(
            text_data=json.dumps({
                "type": "social",
                "category": "friends_leave",
                "player_id": player_id,
                "name": name,
                "status": False
            }))

    @staticmethod
    async def leaveOnline(obj, player_id, name):
        await obj.send(
            text_data=json.dumps({
                "type": "social",
                "category": "online_leave",
                "player_id": player_id,
                "name": name,
                "status": False
            }))

    @staticmethod
    async def addFriend(obj, player_id, name, status):
        await obj.send(
            text_data=json.dumps({
                "type": "social",
                "category": "add_friend",
                "player_id": player_id,
                "name": name,
                "status": status
            }))

    @staticmethod
    async def removeFriend(obj, player_id, name, status):
        await obj.send(
            text_data=json.dumps({
                "type": "social",
                "category": "remove_friend",
                "player_id": player_id,
                "name": name,
                "status": status
            }))

    @staticmethod
    async def infoTreeGame(room_group_name, info, category):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            room_group_name,
            {
                "type": "sendToGroup",
                'rq_type': 'game_info_tree',
                'category': category,
                'info': info
            }
        )

    @staticmethod
    async def infoTreeGameSingle(obj, info, category):
        await obj.send(
            text_data=json.dumps({
                'type': 'game_info_tree',
                'category': category,
                'info': info
                }))

    @staticmethod
    async def tourFinalWaiting(obj):
        await obj.send(
            text_data=json.dumps({
                'type': 'tour_final_waiting'
                }))