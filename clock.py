from time import time
starttime = None
recordtime = None


def gettime():
    return int(time() * 1000)


class MyClock:
    def __init__(self):
        self.starttime = None
        self.pausetime = None
        self.skiptime = 0
        self.pause = False

    def startrecord(self):
        self.starttime = gettime()

    def pauserecord(self):
        self.pausetime = gettime()
        self.pause = True

    def continuerecord(self):
        self.skiptime += gettime()-self.pausetime
        self.pausetime = None
        self.pause = False

    def getrecordstime(self):
        x = gettime()-self.starttime-self.skiptime
        if self.pause:
            return (x-(gettime()-self.pausetime))//1000
        else:
            return x//1000
