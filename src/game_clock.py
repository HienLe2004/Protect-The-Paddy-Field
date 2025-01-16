from setting import *

class Game_Clock(object):
    def __init__(self):
        self.duration = 30
        self.time = self.duration
        self.start = False
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.text = self.font.render(str(int(self.time)), True, (0, 0, 0))
        self.rect = self.text.get_frect(midtop = (SCREEN_WIDTH/2, 10))
    def start_clock(self):
        self.time = self.duration
        self.start = True
    def draw(self, surf):
        surf.blit(self.text, self.rect)

    def update(self, dt):
        if (self.start):
            self.time -= dt
            print(self.time)
            if (self.time <= 0):
                print("end")
                self.start = False
        
        self.text = self.font.render(str(int(self.time)), True, (0, 0, 0))
        self.rect = self.text.get_frect(midtop = (SCREEN_WIDTH/2, 10))

