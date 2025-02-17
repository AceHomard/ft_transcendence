import json


class Request:

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
                "status": category,
                "title": title,
                "message": message
            }))