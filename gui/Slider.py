import pygame
import Colors as c
pygame.init()

class Slider():
    def __init__(self,screen,  name, val, maxi, mini, pos):
        self.screen = screen
        self.val = val  # start value
        self.maxi = maxi  # maximum at slider position right
        self.mini = mini  # minimum at slider position left
        self.xpos = pos  # x-location on screen
        self.ypos = 60
        self.surf = pygame.surface.Surface((200, 75))
        self.hit = False  # the hit attribute indicates slider movement due to mouse interaction
        self.font_name="Segoe Print"
        self.font_size=18
        self.font = pygame.font.SysFont(self.font_name, self.font_size)


        self.txt_surf = self.font.render(name, 1, c.BLACK)
        self.txt_rect = self.txt_surf.get_rect(center=(50, 15))

        self.surf.fill((100, 100, 100))
        pygame.draw.rect(self.surf, c.WHITE, [0, 0, 200, 75], 2)
        pygame.draw.rect(self.surf, c.WHITE, [20, 45, 150, 6], 0)

        self.surf.blit(self.txt_surf, self.txt_rect)  # this surface never changes

        # dynamic graphics - button surface #
        self.button_surf = pygame.surface.Surface((20, 20))
        self.button_surf.fill(c.TRANS)
        self.button_surf.set_colorkey(c.TRANS)
        pygame.draw.circle(self.button_surf, c.BLACK, (10, 10), 7, 0)
        pygame.draw.circle(self.button_surf, c.COLOR_INACTIVE, (10, 10), 5, 0)

    def draw(self):
        """ Combination of static and dynamic graphics in a copy of
    the basic slide surface
    """
        # static
        surf = self.surf.copy()

        # dynamic
        pos = (20+int((self.val-self.mini)/(self.maxi-self.mini)*150), 48)
        self.button_rect = self.button_surf.get_rect(center=pos)
        surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.xpos, self.ypos)  # move of button box to correct screen position

        # screen
        self.screen.blit(surf, (self.xpos, self.ypos))

    def move(self):
        """
    The dynamic part; reacts to movement of the slider button.
    """
        self.val = int((pygame.mouse.get_pos()[0] - self.xpos - 20) / 150 * (self.maxi - self.mini) + self.mini)
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi
