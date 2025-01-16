from setting import *
class Slingshot(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.original_image = pygame.image.load('images/slingshot.png')
        self.image = self.original_image
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.rect = self.image.get_frect(center = (self.x, self.y))
        self.shoot_time = 0
        self.cooldown_duration = 250
        self.can_shoot = True
        self.scale = 1

    def update(self, dt):
        (self.x, self.y) = pygame.mouse.get_pos()
        self.rect.center = (self.x, self.y)

        interval = pygame.time.get_ticks() - self.shoot_time
        if interval >= self.cooldown_duration:
            self.can_shoot = True
            self.image = self.original_image
        else:
            self.scale = 2 - interval / self.cooldown_duration 
            self.image = pygame.transform.rotozoom(self.original_image, 0, self.scale)
        self.rect = self.image.get_frect(midtop = (self.x, self.y))

    def shoot(self):
        self.can_shoot = False
        self.shoot_time = pygame.time.get_ticks()
        self.scale = 2
