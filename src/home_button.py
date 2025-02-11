import pygame

class HomeButton:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 0, 0)  # Red color
        self.text = text
        self.action = action
        self.font = pygame.font.Font(None, 36)  # Font for the button text

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            self.action()  # Call the action when clicked
