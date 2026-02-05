from random import randint
from BlockGroup import *
from const import *


def generateconfig(rect, shape, playernum, where, color):
    blocks = []
    for x in range(len(BLOCK_SHAPE[shape][0])):
        config = {
            'blockcolor': color,
            'rowidx': BLOCK_SHAPE[shape][0][x][0],  # 主型 旋转 各block位置 的x坐标(行）
            'colidx': BLOCK_SHAPE[shape][0][x][1],  # 主型 旋转 各block位置 的y坐标(列）
        }
        if playernum == 1:
            ablock = Block(config['blockcolor'], x, shape, (rect.top, rect.left), config['rowidx'], config['colidx'] + GAME_COL//2)
        elif where == 1:
            ablock = Block(config['blockcolor'], x, shape, (rect.top, rect.left), config['rowidx'], config['colidx']+GAME_COL//3)
        elif where == 2:
            ablock = Block(config['blockcolor'], x, shape, (rect.top, rect.left), config['rowidx'], config['colidx'] + GAME_COL*2//3)
        else:
            ablock = None
        blocks.append(ablock)
    return blocks


def hitcheck(dropBlockGroup, book, fixedblocks):
    droplist = dropBlockGroup.getdropindexes()
    leftlist = dropBlockGroup.getleftindexes()
    rightlist = dropBlockGroup.getrightindexes()
    rotatelist = dropBlockGroup.getrotateindexes()
    # 左移 允许
    releft = True
    for zb in leftlist:  # （高，宽）
        if zb in book or zb[1] < 0:
            dropBlockGroup.leftallow = False
            releft = False
    if releft:
        dropBlockGroup.leftallow = True
    # 右移 允许
    reright = True
    for zb in rightlist:
        if zb in book or zb[1] >= GAME_COL:
            dropBlockGroup.rightallow = False
            reright = False
    if reright:
        dropBlockGroup.rightallow = True
    # 旋转 允许
    rerotate = True
    for zb in rotatelist:
        if zb in book or zb[1] >= GAME_COL or zb[1] < 0 or zb[0] >= GAME_ROW:
            rerotate = False
    if rerotate:
        dropBlockGroup.rotateallow = True
    else:
        dropBlockGroup.rotateallow = False
    # 下落 允许
    redrop = True
    for zb in droplist:
        if zb in book or zb[0] >= GAME_ROW:  # 不能下落
            redrop = False
    if redrop:
        dropBlockGroup.dropallow = True
    else:
        dropBlockGroup.dropallow = False
    # 落地检测
    arrive = False
    for zb in droplist:
        if zb in fixedblocks or zb[0] >= GAME_ROW:  # 到达底部
            arrive = True
    if arrive and dropBlockGroup.arrivetime is None:  # 到达底部且未记录时间
        dropBlockGroup.arrivetime = gettime()
    if dropBlockGroup.arrivetime and gettime()-dropBlockGroup.arrivetime >= 300:
        if arrive:
            return True
        else:
            dropBlockGroup.arrivetime = None
    return False


class Game:
    def __init__(self, playernum, mode, rect, keys, surface):
        self.playernum = playernum
        self.mode = mode
        self.rect = rect
        self.score = 0
        self.keys = keys
        if playernum == 2:
            self.keys = keys[0:len(keys)//2]
            self.keys2 = keys[len(keys)//2:len(keys)]
        self.skills = 0
        self.fixedBlockGroup = FixedBlockGroup()
        self.dropBlockGroup = None
        if playernum == 2:
            self.dropBlockGroup2 = None
        self.dropshape = None
        self.end = 0
        self.surface = surface

    def draw(self):
        _DRAWFONT = pygame.font.SysFont("SimHei", 20)
        scoretextimage = _DRAWFONT.render("得分：" + str(self.score), True, (255, 255, 255))
        self.surface.blit(scoretextimage, (self.rect.left+30, 20 + self.rect.top))
        if self.mode == 2:
            skilltextimage = _DRAWFONT.render("剩余可用技能："+str(self.skills), True, (255, 255, 255))
            self.surface.blit(skilltextimage, (self.rect.left+10, 50+self.rect.top))
        self.fixedBlockGroup.draw(self.surface)
        if self.dropBlockGroup:
            self.dropBlockGroup.draw()
        if self.playernum == 2 and self.dropBlockGroup2:
            self.dropBlockGroup2.draw()

    def generatedropblockgroup(self, where):
        self.dropshape = randint(0, len(BLOCK_SHAPE) - 1)  # 主型编号
        color = randint(0, BlockType.BLOCKMAX - 1)  # 颜色
        blocks = generateconfig(self.rect, self.dropshape, self.playernum, where, color)  # 小方块配置
        if where == 1:
            self.dropBlockGroup = DropBlockGroup(blocks, self.dropshape, self.keys, self.surface)
        elif where == 2:
            self.dropBlockGroup2 = DropBlockGroup(blocks, self.dropshape, self.keys2, self.surface)

    def update(self):
        self.fixedBlockGroup.update()
        if self.dropBlockGroup is None:
            self.generatedropblockgroup(1)
        else:
            self.dropBlockGroup.update()
        if self.playernum == 2:
            if self.dropBlockGroup2 is None:
                self.generatedropblockgroup(2)
            else:
                self.dropBlockGroup2.update()
        if self.mode == 2 and self.skills:  # 存储技能模式
            if pygame.key.get_pressed()[self.keys[0]] and not self.dropBlockGroup.skill:  # 玩家1使用技能
                self.dropBlockGroup.skill = True
                self.skills -= 1
            elif self.playernum == 2 and pygame.key.get_pressed()[self.keys2[0]] and not self.dropBlockGroup2.skill:  # 玩家2（如果有）使用技能
                self.dropBlockGroup2.skill = True
                self.skills -= 1

        check1bg = self.fixedBlockGroup.getblockindexes()
        if self.playernum == 2:
            for b in self.dropBlockGroup2.getblockindexes():
                check1bg.append(b)
        if hitcheck(self.dropBlockGroup, check1bg, self.fixedBlockGroup.getblockindexes()):
            dropbs = self.dropBlockGroup.blocks
            rotate = self.dropBlockGroup.rotate
            # 换班
            for b in dropbs:
                self.fixedBlockGroup.addblocks(b)
            self.dropBlockGroup.clearblocks()
            if self.dropBlockGroup.skill:
                self.usingskill(rotate, dropbs)
                for b in dropbs:
                    b.startblink()
            self.dropBlockGroup = None
            self.checkrow(rotate, dropbs)
            for zb in self.fixedBlockGroup.getblockindexes():  # （高，宽）
                if zb[0] == 0:
                    self.end = -1
        elif self.playernum == 2:
            check2bg = self.fixedBlockGroup.getblockindexes()
            for b in self.dropBlockGroup.getblockindexes():
                check2bg.append(b)
            if hitcheck(self.dropBlockGroup2, check2bg, self.fixedBlockGroup.getblockindexes()):
                dropbs = self.dropBlockGroup2.blocks
                rotate = self.dropBlockGroup2.rotate
                # 换班
                for b in dropbs:
                    self.fixedBlockGroup.addblocks(b)
                self.dropBlockGroup2.clearblocks()
                if self.dropBlockGroup2.skill:
                    self.usingskill(rotate, dropbs)
                    for b in dropbs:
                        b.startblink()
                self.dropBlockGroup2 = None
                self.checkrow(rotate, dropbs)
                for zb in self.fixedBlockGroup.getblockindexes():  # （高，宽）
                    if zb[0] == 0:
                        self.end = -1

    def checkrow(self, rotate, dropbs):  # 查行
        blockcnt = {}
        for row in range(GAME_ROW):  # 左闭右开
            blockcnt[row] = 0
        for b in self.fixedBlockGroup.blocks:
            currow = b.getindex()[0]
            blockcnt[currow] += 1
            if blockcnt[currow] == GAME_COL:  # FULL
                for fb in self.fixedBlockGroup.blocks:
                    x = fb.getindex()[0]
                    if x == currow:
                        fb.startblink()
                if self.mode == 1:
                    self.usingskill(rotate, dropbs)
                if self.mode == 2:
                    self.skills += 1
                self.score += 1

    def usingskill(self, rotate, dropbs):
        opt = self.dropshape
        minx = GAME_ROW
        miny = GAME_COL
        maxx = 0
        maxy = 0
        for b in dropbs:
            minx = min(minx, b.getindex()[0])
            miny = min(miny, b.getindex()[1])
            maxx = max(maxx, b.getindex()[0])
            maxy = max(maxy, b.getindex()[1])
        if opt == 0:  # 方形（炸掉三圈）
            for b in self.fixedBlockGroup.blocks:
                x = b.getindex()[0]
                y = b.getindex()[1]
                if x <= minx and minx - x <= BOOM_RANGE:
                    if y <= miny and miny - y <= BOOM_RANGE:
                        b.startblink()
                    elif y >= maxy and y - maxy <= BOOM_RANGE:
                        b.startblink()
                elif x >= maxx and x - maxx <= BOOM_RANGE:
                    if y <= miny and miny - y <= BOOM_RANGE:
                        b.startblink()
                    elif y >= maxy and y - maxy <= BOOM_RANGE:
                        b.startblink()
        elif opt == 1:  # 长条（消除最下方的三层）
            for b in self.fixedBlockGroup.blocks:
                if b.getindex()[0] >= GAME_ROW - 3:
                    b.startblink()
        elif opt == 2:  # z（右下斜劈）
            for b in self.fixedBlockGroup.blocks:
                if abs((b.getindex()[1] - b.getindex()[0]) - (miny - minx)) <= 2:
                    b.startblink()
        elif opt == 3:  # s（左下斜劈）
            for b in self.fixedBlockGroup.blocks:
                if abs((b.getindex()[1] + b.getindex()[0]) - (miny + minx)) <= 2:
                    b.startblink()
        elif opt == 4 or opt == 5:  # L/J
            if rotate == 0:  # →
                for b in self.fixedBlockGroup.blocks:
                    if b.getindex()[1] >= miny and minx <= b.getindex()[0] <= maxx:
                        b.startblink()
            elif rotate == 1:  # ↓
                for b in self.fixedBlockGroup.blocks:
                    if b.getindex()[1] >= minx and miny <= b.getindex()[1] <= maxy:
                        b.startblink()
            elif rotate == 2:  # ←
                for b in self.fixedBlockGroup.blocks:
                    if b.getindex()[1] <= maxy and minx <= b.getindex()[0] <= maxx:
                        b.startblink()
            elif rotate == 3:  # ↑
                for b in self.fixedBlockGroup.blocks:
                    if b.getindex()[1] <= maxx and miny <= b.getindex()[1] <= maxy:
                        b.startblink()
        elif opt == 6:  # T（竖劈）
            for b in self.fixedBlockGroup.blocks:
                if -1 <= b.getindex()[1] - miny <= 3:
                    b.startblink()

    def showwin(self):
        winfigure = pygame.image.load("picture/win.png")
        winfigure = pygame.transform.scale(winfigure, (self.rect.width, self.rect.height))
        self.surface.blit(winfigure, self.rect)

    def showlose(self):
        losefigure = pygame.image.load("picture/lose.png")
        losefigure = pygame.transform.scale(losefigure, (self.rect.width, self.rect.height))
        self.surface.blit(losefigure, self.rect)

    def showgameover(self):
        overfigure = pygame.image.load("picture/over.png")
        overfigure = pygame.transform.scale(overfigure, (self.rect.width, self.rect.height))
        self.surface.blit(overfigure, self.rect)
