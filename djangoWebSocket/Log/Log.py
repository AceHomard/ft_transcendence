from datetime import datetime
from sty import fg, bg, ef, rs


class Log:
    @staticmethod
    def getTimeNow():
        now = datetime.now()
        return now.strftime("[%d/%m/%Y %H:%M:%S]")

    @staticmethod
    def info(title, msg):
        print(fg.blue + Log.getTimeNow() + str(title) + ": " + fg.white + str(msg))

    @staticmethod
    def error(title, msg):
        print(fg.red + Log.getTimeNow() + str(title) + ": " + fg.white + str(msg))

    @staticmethod
    def debug(title, msg):
        print(fg.da_grey + Log.getTimeNow() + str(title) + ": " + fg.white + str(msg))
