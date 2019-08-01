import pygame
import Colors as c
pygame.init()

class Button():
    def __init__(self,screen, txt, location, action, bg=c.WHITE, fg=c.BLACK, size=(80, 30), font_name="Segoe Print", font_size=20):
        self.screen = screen
        self.color = bg  # the static (normal) color
        self.bg = bg  # actual background color, can change on mouseover
        self.fg = fg  # text color
        self.size = size

        self.font = pygame.font.SysFont(font_name, font_size)
        self.txt = txt
        self.txt_surf = self.font.render(self.txt, 1, self.fg)
        self.txt_rect = self.txt_surf.get_rect(center=[s//2 for s in self.size])

        self.surface = pygame.surface.Surface(size)
        self.rect = self.surface.get_rect(center=location)

        self.call_back_ = action
        self.hit = False

    def draw(self):
        self.mouseover()
        self.pressed()
        self.surface.fill(self.bg)
        self.surface.blit(self.txt_surf, self.txt_rect)
        self.screen.blit(self.surface, self.rect)

    def pressed(self):
        pos = pygame.mouse.get_pos()
        if self.hit:
            self.bg = c.COLOR_INACTIVE
    def mouseover(self):
        self.bg = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = c.GREY

    def call_back(self):
        self.call_back_(self.txt)
