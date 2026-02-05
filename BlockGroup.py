from block import *
from clock import gettime


class DropBlockGroup:  # blockgroup坐标一直不变，变的是block相对于blockgroup的坐标
    def __init__(self, blocks, shape, keys, surface):
        super().__init__()
        self.blocks = blocks
        self.shape = shape
        self.keys = keys
        self.rotate = 0
        self.rotateallow = True
        self.dropallow = True
        self.leftallow = True
        self.rightallow = True
        self.skill = False
        self.time = 0  # 间隔中的时间（即当前时间-下落瞬间）
        self.dropinterval = 800  # 下落间隔
        self.presstime = {}  # 记录各按键按下的时间的字典
        self.arrivetime = None  # 到达底部时间（Game类的需求）
        self.surface = surface

    def draw(self):
        for b in self.blocks:
            if self.skill:  # 开了技能要发白
                b.figure = whiteblock
                b.figure = pygame.transform.scale(b.figure, (Block_width, Block_height))
            b.draw(self.surface)

    def update(self):
        # 下落
        oldtime = self.time
        curtime = gettime()
        difftime = curtime - oldtime
        if difftime >= self.dropinterval:
            self.time = curtime
            if self.dropallow:
                for b in self.blocks:
                    b.drop()
                    b.draw(self.surface)
        # 控制
        self.keyhandler()

    def getblockindexes(self):
        res = []
        for b in self.blocks:
            res.append(b.getindex())
        return res

    def getdropindexes(self):
        res = []
        for b in self.blocks:
            res.append(b.getdropindex())
        return res

    def getrotateindexes(self):
        res = []
        for b in self.blocks:
            res.append(b.getrotateindex())
        return res

    def getleftindexes(self):
        res = []
        for b in self.blocks:
            res.append(b.getleftindex())
        return res

    def getrightindexes(self):
        res = []
        for b in self.blocks:
            res.append(b.getrightindex())
        return res

    # 增删改查
    def getblocks(self):
        return self.blocks

    def clearblocks(self):
        self.blocks = []

    def addblocks(self, newblock):
        self.blocks.append(newblock)

    # 键盘操作及相关限制
    def checkandsetpress(self, key):
        res = False
        if gettime() - self.presstime.get(key, 0) > 80:  # 上次按键时间默认为0
            res = True
        self.presstime[key] = gettime()
        return res

    def keyhandler(self):
        pressed = pygame.key.get_pressed()
        if pressed[self.keys[1]] and self.checkandsetpress(self.keys[1]):
            if self.leftallow:
                for b in self.blocks:
                    b.moveleft()
        elif pressed[self.keys[2]] and self.checkandsetpress(self.keys[2]):
            if self.rightallow:
                for b in self.blocks:
                    b.moveright()
        elif pressed[self.keys[3]] and self.checkandsetpress(self.keys[3]):
            if self.rotateallow:
                for b in self.blocks:
                    b.turn()
                self.rotate += 1
                if self.rotate == len(BLOCK_SHAPE[self.shape]):
                    self.rotate = 0
        elif pressed[self.keys[4]]:
            self.dropinterval = 30
        else:
            self.dropinterval = 800


class FixedBlockGroup:
    def __init__(self):
        super().__init__()
        self.blocks = []

    def draw(self, surface):
        for b in self.blocks:
            b.draw(surface)

    def getblockindexes(self):
        res = []
        for b in self.blocks:
            res.append(b.getindex())
        return res

    def update(self):
        for b in self.blocks:
            b.updateblink()
        flag = 1
        for b in self.blocks:
            if b.blinkcount != 0:
                flag = 0
        if flag:
            self.dodelete()

    def dodelete(self):
        for b in self.blocks:
            if b.blink:
                for i in self.blocks:
                    if i.getindex()[1] == b.getindex()[1] and i.getindex()[0] < b.getindex()[0]:
                        i.drop()
                self.blocks.remove(b)
                del b

        # 增删改查
    def getblocks(self):
        return self.blocks

    def clearblocks(self):
        self.blocks = []

    def addblocks(self, newblock):
        self.blocks.append(newblock)
