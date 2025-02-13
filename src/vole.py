from setting import *

class Vole(pygame.sprite.Sprite):
    vole_image = pygame.image.load('images/vole.png')
    def __init__(self, *groups, x, y):
        super().__init__(*groups)
        self.image = Vole.vole_image
        self.image = pygame.transform.rotozoom(self.image, 0, 2)
        self.x = x
        self.y = y
        self.rect = self.image.get_frect(center = (self.x, self.y))
        self.life_start_time = pygame.time.get_ticks()
        self.life_time = random.randint(2000, 4000)
        self.disappear = False

    def update(self, dt):
        if pygame.time.get_ticks() - self.life_start_time >= self.life_time:
            self.disappear = True
        # else:
        #     print("Play eating animation")

    def dead(self):
        self.disappear = True
        # print("Play dead animation")


