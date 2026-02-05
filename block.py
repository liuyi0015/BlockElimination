from const import *
from clock import *
import pygame.image


class Block:  # （单个方块），图片，相对blockgroup坐标行、列，方块宽、高，初始坐标
    def __init__(self, color, idx, onshape, borderpos, rowid, colid):
        super().__init__()
        self.bgidx = idx
        self.onshape = onshape
        self.rotate = 0
        self.borderpos = borderpos
        self.rowid = rowid
        self.colid = colid
        self.blink = False
        self.blinkcount = 0
        self.blinktime = 0
        self.figure = pygame.image.load(BLOCK_RES[color])
        self.figure = pygame.transform.scale(self.figure, (Block_width, Block_height))
        self.rect = None
        self.updateimagepos()

    def updateimagepos(self):
        self.rect = self.figure.get_rect()  # 内置函数
        self.rect.top = self.borderpos[0]+Block_height*self.rowid
        self.rect.left = self.borderpos[1]+Block_width*self.colid

    def draw(self, surface):
        self.updateimagepos()
        if self.blink and self.blinkcount & 1:
            return
        surface.blit(self.figure, self.rect)

    def turn(self):
        oldx = BLOCK_SHAPE[self.onshape][self.rotate][self.bgidx][0]
        oldy = BLOCK_SHAPE[self.onshape][self.rotate][self.bgidx][1]
        self.rotate += 1
        if self.rotate == len(BLOCK_SHAPE[self.onshape]):
            self.rotate = 0
        newx = BLOCK_SHAPE[self.onshape][self.rotate][self.bgidx][0]
        newy = BLOCK_SHAPE[self.onshape][self.rotate][self.bgidx][1]
        self.rowid += newx - oldx
        self.colid += newy - oldy

    def drop(self):
        self.rowid += 1

    def getindex(self):  # 当前坐标
        return self.rowid, self.colid

    def getdropindex(self):  # 下
        return self.rowid+1, self.colid

    def getrotateindex(self):
        oldx = BLOCK_SHAPE[self.onshape][self.rotate][self.bgidx][0]
        oldy = BLOCK_SHAPE[self.onshape][self.rotate][self.bgidx][1]
        x = self.rotate + 1
        if x == len(BLOCK_SHAPE[self.onshape]):
            x = 0
        newx = BLOCK_SHAPE[self.onshape][x][self.bgidx][0]
        newy = BLOCK_SHAPE[self.onshape][x][self.bgidx][1]
        return self.rowid+newx-oldx, self.colid+newy-oldy

    def getleftindex(self):  # 左
        return self.rowid, self.colid-1

    def getrightindex(self):  # 右
        return self.rowid, self.colid+1

    def moveleft(self):
        self.colid -= 1

    def moveright(self):
        self.colid += 1

    def startblink(self):
        self.blink = True
        self.blinktime = gettime()
        self.blinkcount = 10

    def updateblink(self):
        if self.blink and self.blinkcount != 0:
            difftime = gettime() - self.blinktime
            if difftime >= 100:
                self.blinkcount -= 1
                self.blinktime = gettime()
