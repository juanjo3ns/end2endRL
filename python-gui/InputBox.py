import Colors as c
import pygame
pygame.init()

class InputBox:

    def __init__(self, screen, x, y, w, h, text=''):
        self.screen = screen
        self.pos = x,y
        self.rect = pygame.Rect(x, y, w, h)
        self.color = c.COLOR_INACTIVE
        self.text = text
        self.font_name="Segoe Print"
        self.font_size=18
        self.font = pygame.font.SysFont(self.font_name, self.font_size)

        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = c.COLOR_ACTIVE if self.active else c.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(75, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self):
        # Blit the text.
        self.screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(self.screen, self.color, self.rect, 2)
