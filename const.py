from util import ffind
from pygame.image import load



class BlockType:
    PINK = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4
    BLOCKMAX = 5


BLOCK_RES = {
    BlockType.PINK: "picture/pink_block.jpeg",
    BlockType.RED: "picture/red_block.jpeg",
    BlockType.GREEN: "picture/green_block.jpeg",
    BlockType.BLUE: "picture/blue_block.jpeg",
    BlockType.YELLOW: "picture/yellow_block.jpeg",
}

Block_height = int(ffind("Block_height:"))
Block_width = int(ffind("Block_width:"))
GAME_ROW = int(ffind("rownum:"))
GAME_COL = int(ffind("colnum:"))
WINDOWsheight = Block_height * (GAME_ROW+1)
WINDOWswidth = Block_width * GAME_COL
whiteblock = load("picture/white_block.jpg")
print("窗口大小：%d高x%d宽" % (WINDOWsheight, WINDOWswidth))
print(GAME_COL)
print(GAME_ROW)

BLOCK_SHAPE = [
    [((0, 0), (0, 1), (1, 0), (1, 1))],  # 0.方形（炸掉三圈）
    [((0, 0), (0, 1), (0, 2), (0, 3)), ((0, 0), (1, 0), (2, 0), (3, 0))],  # 1.长条（消除最下方的三层）
    [((0, 0), (0, 1), (1, 1), (1, 2)), ((0, 1), (1, 0), (1, 1), (2, 0))],  # 2.z型（右下斜劈）
    [((0, 1), (1, 0), (1, 1), (0, 2)), ((0, 0), (1, 0), (1, 1), (2, 1))],  # 3.s型（左下斜劈）
    [((0, 0), (1, 0), (2, 0), (2, 1)), ((1, 0), (0, 0), (0, 1), (0, 2)), ((0, 0), (0, 1), (1, 1), (2, 1)),
     ((0, 2), (1, 0), (1, 1), (1, 2))],  # 4.L型
    [((0, 1), (1, 1), (2, 1), (2, 0)), ((0, 0), (1, 0), (1, 1), (1, 2)), ((0, 1), (0, 0), (1, 0), (2, 0)),
     ((0, 0), (0, 1), (0, 2), (1, 2))],  # 5.J型（沿短边铲掉长边碰到的所有方块）
    [((0, 1), (1, 0), (1, 1), (1, 2)), ((0, 0), (1, 0), (2, 0), (1, 1)), ((0, 0), (0, 1), (0, 2), (1, 1)),
     ((0, 1), (1, 0), (1, 1), (2, 1))],  # 6.T型（竖劈）
]

BOOM_RANGE = 3
skillintroduction = ["方形: 炸掉3圈", "长条: 消除最下方的3层", "z型: 右下斜劈", "s型: 左下斜劈", "L型: 用短边拉，铲掉长边碰到的所有方块",
                     "J型: 用短边推，铲掉长边碰到的所有方块", "T型: 竖劈5列", '', "注：技能消除的方块不能得分"]
