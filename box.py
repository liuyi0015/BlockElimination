import pygame.draw


class textButton:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.onclick = False
        self.rect = pygame.Rect(x, y, width, height)
        self.margin = pygame.Rect(x-5, y-5, width+10, height+10)

    def draw(self, screen):
        font = pygame.font.SysFont("SimHei", 30)
        if self.onclick:
            padding_color = (0, 0, 255)  # 深蓝
        else:
            padding_color = (140, 255, 255)  # 天蓝
        margin_color = (0, 140, 0)  # 淡绿
        text_color = (0, 0, 0)
        text_surface = font.render(self.text, True, text_color, padding_color)
        textrect = text_surface.get_rect()
        textrect.center = self.rect.center
        pygame.draw.rect(screen, margin_color, self.margin)
        pygame.draw.rect(screen, padding_color, self.rect)
        screen.blit(text_surface, textrect)

    def is_clicked(self, mousepos):
        if self.margin.collidepoint(mousepos):
            self.onclick = True
            return True
        else:
            self.onclick = False
            return False

    def updatetext(self, newtext):
        self.text = newtext


class imageButton:
    def __init__(self, onurl, offurl, x, y, width, height):
        self.onurl = onurl
        self.offurl = offurl
        self.look = True
        self.rect = pygame.Rect(x+2, y+2, width-4, height-4)
        self.margin = pygame.Rect(x, y, width, height)
        self.figure = pygame.image.load(onurl)
        self.figure = pygame.transform.scale(self.figure, (self.rect.width, self.rect.height))

    def draw(self, screen):
        margin_color = (140, 255, 155)
        pygame.draw.rect(screen, margin_color, self.margin)
        screen.blit(self.figure, self.rect)

    def updateimage(self):
        if self.look:
            self.figure = pygame.image.load(self.offurl)
            self.look = False
        else:
            self.figure = pygame.image.load(self.onurl)
            self.look = True
        self.figure = pygame.transform.scale(self.figure, (self.rect.width, self.rect.height))

    def is_clicked(self, mousepos):
        return self.margin.collidepoint(mousepos)


class InputBox:
    def __init__(self, origintext, x, y, width, height):
        self.text = origintext
        self.onclick = False
        self.rect = pygame.Rect(x, y, width, height)
        self.margin = pygame.Rect(x - 5, y - 5, width + 10, height + 10)

    def draw(self, screen):
        font = pygame.font.SysFont("SimHei", 30)
        if self.onclick:
            padding_color = (255, 255, 0)
        else:
            padding_color = (255, 255, 200)
        margin_color = (0, 140, 0)  # 淡绿
        text_color = (0, 0, 0)
        text_surface = font.render(self.text, True, text_color, padding_color)
        textrect = text_surface.get_rect()
        textrect.center = self.rect.center
        pygame.draw.rect(screen, margin_color, self.margin)
        pygame.draw.rect(screen, padding_color, self.rect)
        screen.blit(text_surface, textrect)

    def dealevent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.margin.collidepoint(pygame.mouse.get_pos()):
                self.onclick = True
            else:
                self.onclick = False
        elif self.onclick and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
