import pygame

class PlayButton:
    def __init__(self, x, y, size, action):
        self.points = [
            (x, y),  # Bottom left
            (x, y + size),  # Bottom right
            (x + size, y + size/2)  # Top
        ]
        self.color = (0, 255, 0)  # Green
        self.action = action
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        pygame.draw.polygon(surface, self.color, self.points)
        center_x = (self.points[0][0] + self.points[1][0] + self.points[2][0]) / 3
        center_y = (self.points[0][1] + self.points[1][1] + self.points[2][1]) / 3
        text_surface = self.font.render("Play", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(center_x, center_y))
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        # Check if the click position is within the triangle using a point-in-triangle algorithm
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        b1 = sign(pos, self.points[0], self.points[1]) < 0.0
        b2 = sign(pos, self.points[1], self.points[2]) < 0.0
        b3 = sign(pos, self.points[2], self.points[0]) < 0.0

        if b1 == b2 == b3:
            self.action()  # Call the action when clicked
