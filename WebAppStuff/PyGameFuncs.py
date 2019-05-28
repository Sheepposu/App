import pygame

class Screen_Display():
    def text_objects(text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def message_display(gD, text, size, color, centerX, centerY):
        font = pygame.font.SysFont('arial', size)
        textSurf, TextRect = Screen_Display.text_objects(text, font, color)
        TextRect.center = ((centerX),(centerY))
        gD.blit(textSurf, TextRect)

class Button():
    def __init__(self, rect, text, textsize, textcolor):
        self.rect = rect
        self.font = pygame.font.SysFont('arial', textsize)
        self.textSurf, self.textRect = Screen_Display.text_objects(text, self.font, textcolor)
        self.textRect.center = ((rect[0] + (rect[2]/2), rect[1] + (rect[3]/2)))

    def draw(self, gD, ButColor):
        pygame.draw.rect(gD, ButColor, (self.rect))
        gD.blit(self.textSurf, self.textRect)

    def optClick(self, gD, ShadowColor, ButColor, command=None, command2=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.rect[0] + self.rect[2] > mouse[0] > self.rect[0] and self.rect[1] + self.rect[3] > mouse[1] > self.rect[1]:
            pygame.draw.rect(gD, ShadowColor, (self.rect))
            gD.blit(self.textSurf, self.textRect)
            if click[0] == 1:
                    if command != None:
                        command()
                    if command2 != None:
                        command2()
            else:
                pygame.draw.rect(gD, ButColor, (self.rect))
                gD.blit(self.textSurf, self.textRect)

class InvisButton():
    def __init__(self, rect):
        self.rect = rect

    def optClick(self, command=None, command2=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.rect[0] + self.rect[2] > mouse[0] > self.rect[0] and self.rect[1] + self.rect[3] > mouse[1] > self.rect[1]:
            if click[0] == 1:
                    if command != None:
                        command()
                    if command2 != None:
                        command2()

