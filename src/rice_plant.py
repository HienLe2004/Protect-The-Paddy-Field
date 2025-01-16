from setting import *
from vole import Vole
rice_plant_image = pygame.image.load('images/rice.png')

class RicePlant(pygame.sprite.Sprite):
    def __init__(self, *groups, x, y):
        super().__init__(*groups)
        self.image = rice_plant_image
        self.x = x
        self.y = y
        self.rect = self.image.get_frect(midbottom = (self.x, self.y))
        self.attack_time = pygame.time.get_ticks()
        self.cooldown_duration = random.randint(1000, 7000)
        self.attacker = None

    def update(self, dt):
        if not self.attacker:
            if pygame.time.get_ticks() - self.attack_time >= self.cooldown_duration:
                self.attack_time = pygame.time.get_ticks()
                self.attacker = Vole(self.groups(), x = self.x, y = self.y)
        else:
            if self.attacker.disappear:
                self.cooldown_duration = random.randint(2000,7000)
                self.attacker.kill()
                self.attacker = None
                self.attack_time = pygame.time.get_ticks()
            # else:
            #     print("Play being attacked animation")
