from setting import *
from slingshot import Slingshot
from rice_plant import RicePlant
from score import Score
from game_clock import Game_Clock

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Protect The Paddy Field')
        pygame.display.set_icon(pygame.image.load('images/rice.png'))
        self.clock = pygame.time.Clock() 
        self.running = True
        self.background_image = pygame.image.load('images/background.jpg')
        self.background_image = pygame.transform.scale(self.background_image, self.screen.get_size())
        pygame.mouse.set_visible(False)
        # sounds
        self.vole_sounds = [pygame.mixer.Sound(f'sounds/vole{i + 1}.wav') for i in range(3)]
        self.shooting_sounds = pygame.mixer.Sound('sounds/shoot.wav')
        self.background_music = pygame.mixer.Sound('sounds/background.mp3')
        self.background_music.set_volume(0.5)
        self.background_music.play(-1)

        #sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()

        #instantiate game object
        self.rice_plant_group = []
        for row in range(3):
            yPos = SCREEN_HEIGHT * (row + 1 - 0.25) / 3 
            for col in range(4):
                xPos = SCREEN_WIDTH * (2 * col + 1) / 8 
                self.rice_plant_group.append(RicePlant(self.all_sprites, x = xPos, y = yPos))
        self.slingshot = Slingshot(self.player_sprites)
        self.score = Score()
        self.game_clock = Game_Clock()
        self.game_state = Game_State.PLAYING

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.game_clock.start:
                        self.game_clock.start_clock()
                if event.type == pygame.MOUSEBUTTONDOWN and self.slingshot.can_shoot:
                    self.slingshot.shoot()
                    hit = False
                    for rice_plant in self.rice_plant_group:
                        if rice_plant.attacker is not None and not rice_plant.attacker.disappear:
                            if (rice_plant.attacker.rect.collidepoint(pygame.mouse.get_pos())):
                                rice_plant.attacker.dead()
                                hit = True
                    self.shooting_sounds.play()
                    if hit:
                        # print("hit")
                        self.score.set_hit(self.score.hit + 1)
                        self.play_vole_dead_sound()
                    else:
                        # print("miss")
                        self.score.set_miss(self.score.miss + 1)
                            

            self.game_clock.update(dt)
            self.all_sprites.update(dt)
            self.player_sprites.update(dt)
            
            self.screen.fill((200, 200, 200))
            self.all_sprites.draw(self.screen)
            self.score.draw(self.screen)
            self.game_clock.draw(self.screen)
            self.player_sprites.draw(self.screen)
            pygame.display.update()
        pygame.quit()

    def play_vole_dead_sound(self):
        pygame.time.delay(100)
        index = random.randint(0, len(self.vole_sounds) - 1)
        self.vole_sounds[index].play()

class Game_State(enumerate):
    MENU = 0
    STARTING = 1
    PLAYING = 2
    GAME_OVER = 3

if __name__ == '__main__':
    game = Game()
    game.run()