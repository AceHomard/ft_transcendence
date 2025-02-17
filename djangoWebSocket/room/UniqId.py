from datetime import datetime, timezone
import random


class Uniqid:

    @staticmethod
    def __getRandom():
        random_number = random.randint(0, 99)
        formatted_number = str(random_number).zfill(2)
        return formatted_number

    @staticmethod
    def getUnixTimeStamp():
        now_utc = datetime.now(timezone.utc)
        unix_timestamp = int(now_utc.timestamp())
        return unix_timestamp

    @staticmethod
    def generate():
        uniqid = Uniqid.__getRandom() + Uniqid.__getRandom()
        uniqid += str(Uniqid.getUnixTimeStamp())
        uniqid += Uniqid.__getRandom() + Uniqid.__getRandom()
        return str(int(uniqid))
