from sys import exit
from box import textButton, imageButton, InputBox
from game import Game
from keyboard import hook, unhook
import pygame
from const import *
from clock import MyClock
from util import keynum, ffind, fromlinefind

pygame.init()

def showtext(text, center, bgcolor, screen):
    font = pygame.font.SysFont("SimHei", 25)
    text_figure = font.render(text, True, (255, 255, 255), bgcolor)
    text_rect = text_figure.get_rect()
    text_rect.center = center
    screen.blit(text_figure, text_rect)


def setbuttons(line, keytype):
    buttons = []
    for i in range(5):
        usekey = fromlinefind(":", i + keytype * 5)
        buttons.append(
            textButton(usekey, WINDOWswidth // 4 + (i * 3 * Block_width), line, 3 * Block_width, Block_height))
    return buttons


def getkeys(playernum):
    if playernum == 1:
        return [keynum(ffind("Skill_Key:")), keynum(ffind("Left_Key:")), keynum(ffind("Right_Key:")),
                keynum(ffind("Up_Key:")), keynum(ffind("Down_Key:"))]
    elif playernum == 2:
        return [keynum(ffind("Skill_Key1:")), keynum(ffind("Left_Key1:")), keynum(ffind("Right_Key1:")),
                keynum(ffind("Up_Key1:")), keynum(ffind("Down_Key1:")),
                keynum(ffind("Skill_Key2:")), keynum(ffind("Left_Key2:")), keynum(ffind("Right_Key2:")),
                keynum(ffind("Up_Key2:")), keynum(ffind("Down_Key2:"))]


def single_game_window(playernum, gamemode):
    pygame.init()
    window = pygame.display.set_mode((WINDOWswidth, WINDOWsheight))
    pygame.display.set_caption("俄罗斯方块")
    controlkeys = getkeys(playernum)
    game = Game(playernum, gamemode, pygame.Rect(0, Block_height, WINDOWswidth, WINDOWsheight-Block_height), controlkeys, window)
    temp_button = imageButton("picture/pause.jpeg", "picture/continue.jpeg", WINDOWswidth // 3, 0, Block_width, Block_height)
    myclock = MyClock()
    myclock.startrecord()
    tempgame = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("QUIT退出")
                exit()
            # 暂停
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and temp_button.is_clicked(event.pos):
                temp_button.updateimage()
                if tempgame:
                    tempgame = False
                    myclock.continuerecord()
                else:
                    tempgame = True
                    myclock.pauserecord()
        if game.end:
            continue
        if not tempgame:
            game.update()
        _DRAWFONT = pygame.font.SysFont("SimHei", 20)
        timetextimage = _DRAWFONT.render("用时：" + str(myclock.getrecordstime())+'s', True, (255, 255, 255))
        window.fill((0, 0, 0))
        top_rect = pygame.Rect(0, 0, WINDOWswidth, Block_height)
        pygame.draw.rect(window, (0, 0, 150), top_rect)
        temp_button.draw(window)
        if tempgame:
            showtext("继续", (WINDOWswidth // 3 + 2 * Block_width, Block_height // 2), (0, 0, 150), window)
        else:
            showtext("暂停", (WINDOWswidth // 3 + 2 * Block_width, Block_height // 2), (0, 0, 150), window)
        window.blit(timetextimage, (WINDOWswidth * 2 // 3, 0))
        game.draw()
        if game.end:
            game.showgameover()
        pygame.display.update()


def battle_game_window(gamemode, keeptime):
    pygame.init()
    battlewidth = 2*WINDOWswidth+Block_width
    window = pygame.display.set_mode((battlewidth, WINDOWsheight))
    pygame.display.set_caption("俄罗斯方块")
    top_rect = pygame.Rect(0, 0, battlewidth, 60)
    left_game_rect = pygame.Rect(0, Block_height, WINDOWswidth, WINDOWsheight)
    right_game_rect = pygame.Rect(WINDOWswidth+Block_width, Block_height, WINDOWswidth, WINDOWsheight)
    controlkeys = getkeys(2)
    game1 = Game(1, gamemode, left_game_rect, controlkeys[0:len(controlkeys)//2], window)
    game2 = Game(1, gamemode, right_game_rect, controlkeys[len(controlkeys)//2:len(controlkeys)], window)
    temp_button = imageButton("picture/pause.jpeg", "picture/continue.jpeg", battlewidth//2-Block_width//2, 0, Block_width, Block_height)
    tempgame = False
    myrecord = MyClock()
    myrecord.startrecord()
    lasttime = keeptime
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("QUIT退出")
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and temp_button.is_clicked(event.pos):
                temp_button.updateimage()
                if tempgame:
                    tempgame = False
                    myrecord.continuerecord()
                else:
                    tempgame = True
                    myrecord.pauserecord()
        if game1.end or game2.end:
            continue
        _DRAWFONT = pygame.font.SysFont("SimHei", 20)
        if lasttime != 0:
            lasttime = keeptime - myrecord.getrecordstime()
        elif game1.score > game2.score:
            game1.end = 1
            game2.end = -1
        elif game1.score < game2.score:
            game1.end = -1
            game2.end = 1
        if lasttime:
            timetextimage = _DRAWFONT.render("剩余时间：" + str(lasttime)+'s', True, (255, 255, 255))
        elif not game1.end and not game2.end:
            timetextimage = _DRAWFONT.render("加时赛：最快得分的赢", True, (255, 255, 255))
        else:
            timetextimage = _DRAWFONT.render("剩余时间：0s", True, (255, 255, 255))
        if not tempgame:
            game1.update()
            game2.update()
        pygame.draw.rect(window, (0, 0, 0), top_rect)
        pygame.draw.line(window, (255, 255, 0), (battlewidth // 2, Block_height), (battlewidth // 2, WINDOWsheight), Block_width)
        #                 窗口，       颜色，                        上，                      下，              宽
        pygame.draw.rect(window, (0, 100, 100), left_game_rect)
        pygame.draw.rect(window, (0, 0, 100), right_game_rect)
        showtext("对战模式", (Block_width*2, Block_height//2), (0, 0, 0), window)
        temp_button.draw(window)
        if tempgame:
            showtext("继续", (battlewidth // 2 + Block_width*3//2, Block_height // 2), (0, 0, 0), window)
        else:
            showtext("暂停", (battlewidth // 2 + Block_width*3//2, Block_height // 2), (0, 0, 0), window)
        window.blit(timetextimage, (battlewidth*5//6, 0))
        game1.draw()
        game2.draw()
        if game1.end or game2.end:
            if game1.end == -1:
                game1.showlose()
                game2.showwin()
            elif game2.end == -1:
                game2.showlose()
                game1.showwin()
        pygame.display.flip()


def selectmode(title, options):
    pygame.init()
    screen = pygame.display.set_mode((WINDOWswidth, WINDOWsheight))  # flags=pygame.FULLSCREEN
    pygame.display.set_caption(title)
    mode = None
    buttons = []
    for i in range(len(options)):
        button_width = 200
        button_height = 80
        buttons.append(
            textButton(options[i], (WINDOWswidth - button_width) // 2, 100 * (i + 1), button_width, button_height))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("QUIT退出")
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i in range(len(buttons)):
                    if buttons[i].is_clicked(event.pos):
                        mode = i
        if mode is not None:
            break
        for i in range(len(buttons)):
            buttons[i].is_clicked(pygame.mouse.get_pos())
        screen.fill((0, 0, 0))
        for button in buttons:
            button.draw(screen)
        pygame.display.update()
    pygame.quit()
    return mode


def inputtimelimit():
    pygame.init()
    window = pygame.display.set_mode((WINDOWswidth, WINDOWsheight))  # flags=pygame.FULLSCREEN
    pygame.display.set_caption("自定义时限")
    timebox = InputBox("", (WINDOWswidth - 200) // 2, 200, 200, 80)
    finishbutton = textButton("开始游戏", (WINDOWswidth - 140) // 2, 300, 140, 80)
    tips = "输入整数！"
    tipon = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("QUIT退出")
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and finishbutton.is_clicked(event.pos):
                try:
                    return int(timebox.text)
                except ValueError:
                    tipon = True
                    continue
            timebox.dealevent(event)
        finishbutton.is_clicked(pygame.mouse.get_pos())
        window.fill((0, 0, 0))
        if tipon:
            showtext(tips, (WINDOWswidth*4//5, 250), (0, 0, 0), window)
        showtext("输入对战时间(s)", (WINDOWswidth//2, 100), (0, 0, 0), window)
        timebox.draw(window)
        finishbutton.draw(window)
        pygame.display.flip()


def setting():
    pygame.init()
    window = pygame.display.set_mode((WINDOWswidth, WINDOWsheight))
    pygame.display.set_caption("设置")
    bgimage = pygame.image.load("picture/setting_background.png")
    bgimage = pygame.transform.scale(bgimage, (WINDOWswidth, WINDOWsheight))
    returnbutton = textButton("返回", WINDOWswidth - 2 * Block_width, WINDOWsheight // 5, Block_width, Block_height)
    buttons0 = setbuttons(WINDOWsheight // 2 - Block_height, 0)
    buttons1 = setbuttons(WINDOWsheight * 2 // 3 - Block_height // 2, 1)
    buttons2 = setbuttons(WINDOWsheight * 7 // 8 - Block_height * 3 // 2, 2)
    editkey = None
    editline = None

    def func(event):
        if editkey is None:
            return
        with open("data", "r+") as f:
            content = list(f.read())
            line = 0
            i = 0
            while i < len(content):
                if content[i] == '\n':
                    line += 1
                elif line == editline and content[i] == ':':
                    break
                i += 1
            i += 1
            while content[i] != '\n':
                content.pop(i)
            content.insert(i, event.name)
            f.truncate(0)
            f.seek(0)
            f.write(''.join(content))
        editkey.updatetext(event.name)

    hook(func)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("QUIT退出")
                unhook(func)
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if returnbutton.is_clicked(event.pos):
                    pygame.quit()
                    unhook(func)
                    return
                for i in range(len(buttons0)):
                    if buttons0[i].is_clicked(event.pos):
                        if editkey is not None:
                            editkey.onclick = False
                        editkey = buttons0[i]
                        editkey.onclick = True
                        editline = i
                for i in range(len(buttons1)):
                    if buttons1[i].is_clicked(event.pos):
                        if editkey is not None:
                            editkey.onclick = False
                        editkey = buttons1[i]
                        editkey.onclick = True
                        editline = i + 5
                for i in range(len(buttons2)):
                    if buttons2[i].is_clicked(event.pos):
                        if editkey is not None:
                            editkey.onclick = False
                        editkey = buttons2[i]
                        editkey.onclick = True
                        editline = i + 10
        window.fill((0, 0, 0))
        window.blit(bgimage, bgimage.get_rect())
        showtext("(点击按钮后按键即可更改)", (WINDOWswidth//2, WINDOWsheight*8//9), (100, 0, 0), window)
        returnbutton.draw(window)
        for i in range(5):
            buttons0[i].draw(window)
        for i in range(5):
            buttons1[i].draw(window)
        for i in range(5):
            buttons2[i].draw(window)
        pygame.display.flip()


def gamehelp():
    pygame.init()
    window = pygame.display.set_mode((WINDOWswidth, WINDOWsheight))
    pygame.display.set_caption("帮助")
    returnbutton = textButton("返回", (WINDOWswidth - Block_width) // 2, WINDOWsheight * 3 // 4, Block_width,
                              Block_height)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("QUIT退出")
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if returnbutton.is_clicked(event.pos):
                    pygame.quit()
                    return
        n = len(skillintroduction)
        showtext("技能说明", (WINDOWswidth // 2, WINDOWsheight // (2 * n)), (0, 0, 0), window)
        for i in range(n):
            showtext(skillintroduction[i], (WINDOWswidth // 2, WINDOWsheight * (i + 1) // (2 * n) + WINDOWsheight // n),
                     (0, 0, 0), window)
        returnbutton.draw(window)
        pygame.display.flip()


def logo():
    try:
        window = pygame.display.set_mode((WINDOWswidth, WINDOWsheight))
        pygame.display.set_caption("俄罗斯方块")
        font = pygame.font.SysFont("SimHei", 60)
        text_figure = font.render("制作人：liuyi", True, (255, 255, 255), (0, 0, 0))
        text_rect = text_figure.get_rect()
        text_rect.center = (WINDOWswidth//2, WINDOWsheight//4)
        mood = pygame.image.load("picture/logo.png")
        mood = pygame.transform.scale(mood, (WINDOWswidth//2, WINDOWsheight//2))
        mood_rect = mood.get_rect()
        mood_rect.center = (WINDOWswidth//2, WINDOWsheight*2//3)
        window.blit(text_figure, text_rect)
        window.blit(mood, mood_rect)
        pygame.display.flip()
        # 使用 pygame 时钟替代 time.sleep
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 2000:  # 毫秒
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            clock.tick(60)  # 控制帧率
    except Exception as e:
        print("Error:", e)


def menu():
    while True:
        x = selectmode("主菜单", ["开始游戏", "设置", "帮助"])
        if x == 0:
            break
        elif x == 1:
            setting()
        elif x == 2:
            gamehelp()


if __name__ == '__main__':
    logo()
    menu()
    playernum = selectmode("选择游戏模式", ["单人模式", "双人模式"]) + 1
    print("人数" + str(playernum))
    relation = None
    keeptime = -1
    if playernum == 2:
        relation = selectmode("选择游戏方式", ["限时对战", "合作协同"])
        print("游戏方式" + str(relation))
        if relation == 0:
            keeptime = inputtimelimit()
    gamemode = selectmode("选择游戏玩法", ["无技能模式", "即时技能模式", "存储技能模式"])
    print("游戏模式:" + str(gamemode))
    if relation == 0:
        battle_game_window(gamemode, keeptime)
    else:
        single_game_window(playernum, gamemode)

