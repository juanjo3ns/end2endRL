import pygame
import Colors as c
pygame.init()

class CheckBox():
    def __init__(self,screen, location, bg=c.WHITE,  size=(10,10)):
        self.screen = screen
        self.color = bg  # the static (normal) color
        self.bg = bg  # actual background color, can change on mouseover
        self.size = size
        self.surface = pygame.surface.Surface(size)
        self.rect = self.surface.get_rect(center=location)

        self.hit = False

    def draw(self):
        self.pressed()
        self.surface.fill(self.bg)
        self.screen.blit(self.surface, self.rect)

    def pressed(self):
        self.bg = self.color
        pos = pygame.mouse.get_pos()
        if self.hit:
            self.bg = c.COLOR_INACTIVE  # mouseover color
