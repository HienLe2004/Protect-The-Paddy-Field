import random
import pygame

#import
rice_plant_image = pygame.image.load('images/rice.png')
vole_image = pygame.image.load('images/mouse.png')

class Slingshot(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.original_image = pygame.image.load('images/slingshot.png')
        self.image = self.original_image
        self.x = screen.get_width() / 2
        self.y = screen.get_height() / 2
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
                self.attacker = Vole(all_sprites, x = self.x, y = self.y)
        else:
            if self.attacker.disappear:
                self.cooldown_duration = random.randint(2000,7000)
                self.attacker.kill()
                self.attacker = None
                self.attack_time = pygame.time.get_ticks()


class Vole(pygame.sprite.Sprite):
    def __init__(self, *groups, x, y):
        super().__init__(*groups)
        self.image = vole_image
        self.x = x
        self.y = y
        self.rect = self.image.get_frect(center = (self.x, self.y))
        self.life_start_time = pygame.time.get_ticks()
        self.life_time = random.randint(2000, 4000)
        self.disappear = False

    def update(self, dt):
        if pygame.time.get_ticks() - self.life_start_time >= self.life_time:
            self.disappear = True

    def dead(self):
        self.disappear = True
        print("dead")

class Score(object):
    def __init__(self):
        self.miss = 0
        self.hit = 0
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.text = self.font.render("Hit: " + str(self.hit) + " Miss: " + str(self.miss), True, (0, 0, 0))
        self.rect = self.text.get_frect(topleft = (10, 10))

    def draw(self, surf):
        surf.blit(self.text, self.rect)

    def set_hit(self, hit):
        self.hit = hit
        self.text = self.font.render("Hit: " + str(self.hit) + " Miss: " + str(self.miss), True, (0, 0, 0))
        self.rect = self.text.get_frect(topleft = (10, 10))
    
    def set_miss(self, miss):
        self.miss = miss
        self.text = self.font.render("Hit: " + str(self.hit) + " Miss: " + str(self.miss), True, (0, 0, 0))
        self.rect = self.text.get_frect(topleft = (10, 10))


pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Protect The Paddy Field')
pygame.display.set_icon(pygame.image.load('images/rice.png'))
background_image = pygame.image.load('images/background.jpg')
background_image = pygame.transform.scale(background_image, screen.get_size())
clock = pygame.time.Clock()
running = True
dt = 0

all_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
rice_plant_group = []
for row in range(3):
    yPos = screen.get_height() * (row + 1 - 0.25) / 3 
    for col in range(4):
        xPos = screen.get_width() * (2 * col + 1) / 8 
        rice_plant_group.append(RicePlant(all_sprites, x = xPos, y = yPos))

slingshot = Slingshot(player_sprites)
pygame.mouse.set_visible(False)
score = Score()

while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and slingshot.can_shoot:
            slingshot.shoot()
            hit = False
            for rice_plant in rice_plant_group:
                if rice_plant.attacker is not None and not rice_plant.attacker.disappear:
                    if (rice_plant.attacker.rect.collidepoint(pygame.mouse.get_pos())):
                        rice_plant.attacker.dead()
                        hit = True
            if hit:
                print("hit")
                score.set_hit(score.hit + 1)
            else:
                print("miss")
                score.set_miss(score.miss + 1)
                    

    all_sprites.update(dt)
    player_sprites.update(dt)
    
    # screen.blit(background_image, (0, 0))
    screen.fill((200, 200, 200))
    all_sprites.draw(screen)
    score.draw(screen)
    player_sprites.draw(screen)
    pygame.display.update()


pygame.quit()