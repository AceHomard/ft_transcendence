import json
from channels.layers import get_channel_layer


class ConsumerRequest:

    @staticmethod
    async def connection(obj):
        await obj.send(
            text_data=json.dumps({
                "type": "connection_etalished",
                "message": "Game Connected"
                }))

    @staticmethod
    async def playerSide(obj, side):
        await obj.send(
            text_data=json.dumps({
                "type": "player_side",
                "side": side
            }))

    @staticmethod
    async def playerMove(room_group_name, player_y, playerId):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            room_group_name,
            {
                "type": "sendToGroupGame",
                'action': 'movement_correction',
                'movement_correction': player_y,
                'player_id': playerId,
            }
        )

    @staticmethod
    async def ballMove(room_group_name, ball):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            room_group_name,
            {
                "type": "sendToGroupGame",
                'action': 'movement_ball',
                'ball_x': ball.x,
                'ball_y': ball.y,
                'ball_r': ball.r,
                'ball_speed': ball.speed,
            }
        )

    @staticmethod
    async def startGame(room_group_name):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            room_group_name,
            {
                "type": "sendToGroupGame",
                'action': 'start_game',
            }
        )

    @staticmethod
    async def endGame(room_group_name, winner_id):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            room_group_name,
            {
                "type": "sendToGroupGame",
                'action': 'end_game',
                "winner_id": winner_id
            }
        )

    @staticmethod
    async def scoreGame(room_group_name, score_player_a, score_player_b):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            room_group_name,
            {
                "type": "sendToGroupGame",
                'action': 'score_game',
                'score_player_a': score_player_a,
                'score_player_b': score_player_b,
            }
        )

    @staticmethod
    async def infoTimeGame(room_group_name, time):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            room_group_name,
            {
                "type": "sendToGroupGame",
                'action': 'game_info_timer',
                'time': time
            }
        )

    @staticmethod
    async def GameSide(room_group_name, info):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            room_group_name,
            {
                "type": "sendToGroupGame",
                'action': 'game_side_info',
                'info': info
            }
        )
