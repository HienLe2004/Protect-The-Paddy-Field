import pygame
import random
from setting import *
from slingshot import Slingshot
from rice_plant import RicePlant
from score import Score
from game_clock import Game_Clock
from play_button import PlayButton
from home_button import HomeButton
from quit_button import QuitButton
from home_button import HomeButton  # Make sure to import the HomeButton class

class Game_Over:
    def __init__(self, screen, game_state_manager, score):
        self.screen = screen
        self.game_state_manager = game_state_manager
        self.score = score
        self.font = pygame.font.Font("freesansbold.ttf", 36)
        self.buttons = {
            "menu": pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50),
            "replay": pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50)
        }
        self.cursor_img = pygame.image.load('images/slingshot.png').convert_alpha()

    def draw(self):
        self.screen.fill((50, 50, 50))
        score_text = self.font.render(f"HIT: {self.score.hit} MISS: {self.score.miss}", True, (255, 255, 255))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 3))
        
        for key, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (200, 200, 200), rect)
            button_text = self.font.render(key.upper(), True, (0, 0, 0))
            self.screen.blit(button_text, (rect.x + 50, rect.y + 10))
        
        cursor_pos = pygame.mouse.get_pos()
        cursor_rect = self.cursor_img.get_rect(center=cursor_pos)
        self.screen.blit(self.cursor_img, cursor_rect)
        pygame.display.flip()

    def run(self, dt):
        running = True
        pygame.mouse.set_visible(False)
        while running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state_manager.set_state('quit')
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttons["menu"].collidepoint(event.pos):
                        self.game_state_manager.set_state('main_menu')
                        running = False
                    elif self.buttons["replay"].collidepoint(event.pos):
                        self.game_state_manager.set_state('gameplay')
                        running = False

class Game_Play:
    def __init__(self, screen, game_state_manager):
        # setup
        self.screen = screen
        self.game_state_manager = game_state_manager
        pygame.mouse.set_visible(False)
        self.running = True
        
        # sounds
        self.vole_sounds = [pygame.mixer.Sound(f'./sounds/vole{i + 1}.wav') for i in range(3)]
        self.shooting_sounds = pygame.mixer.Sound('./sounds/shoot.wav')
        self.background_music = pygame.mixer.Sound('./sounds/background.mp3')
        self.background_music.set_volume(0.5)
        self.background_music.play(-1)

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()

        # instantiate game object
        self.rice_plant_group = []
        for row in range(3):
            yPos = SCREEN_HEIGHT * (row + 1 - 0.25) / 3 
            for col in range(4):
                xPos = SCREEN_WIDTH * (2 * col + 1) / 8 
                self.rice_plant_group.append(RicePlant(self.all_sprites, x=xPos, y=yPos))
        self.slingshot = Slingshot(self.player_sprites)
        self.score = Score()
        self.game_clock = Game_Clock()
        
        # Create Home Button
        self.home_button = HomeButton(SCREEN_WIDTH - 120, 20, 100, 50, 'Home', self.return_to_menu)

    def return_to_menu(self):
        self.running = False  # Stop the game loop
        pygame.mouse.set_visible(True)
        self.game_state_manager.set_state('main_menu')  # Change state to main menu


    def run(self, dt):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game_state_manager.set_state('quit')

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
                            
            self.game_clock.update()
            if self.game_clock.time_up:
                print("TIME OUT")
                self.game_state_manager.set_state('game_over')
                self.running = False
                break

                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_SPACE and not self.game_clock.start:
                #         self.game_clock.start_clock()
                # if event.type == pygame.MOUSEBUTTONDOWN:
                # 	if event.button == 1:  # Left mouse button
                #     # Check if home button is clicked
		        #         if self.home_button.is_clicked(event.pos):
		        #             continue  # Do not proceed further if home button was clicked
		        #         # Check if slingshot can shoot
		        #         if self.slingshot.can_shoot:
		        #             self.slingshot.shoot()
		        #             hit = False
		        #         for rice_plant in self.rice_plant_group:
		        #             if rice_plant.attacker is not None and not rice_plant.attacker.disappear:
		        #                 if (rice_plant.attacker.rect.collidepoint(pygame.mouse.get_pos())):
		        #                     rice_plant.attacker.dead()
		        #                     hit = True
		        #         self.shooting_sounds.play()
		        #         if hit:
		        #             self.score.set_hit(self.score.hit + 1)
		        #             self.play_vole_dead_sound()
		        #         else:
		        #             self.score.set_miss(self.score.miss + 1)
            # self.game_clock.update(dt)

            self.all_sprites.update(dt)
            self.player_sprites.update(dt)
            
            self.screen.fill((200, 200, 200))
            self.all_sprites.draw(self.screen)
            self.score.draw(self.screen)
            self.game_clock.draw(self.screen)
            self.player_sprites.draw(self.screen)
            # self.home_button.draw(self.screen)  # Draw the home button
            pygame.display.update()
    def play_vole_dead_sound(self):
        pygame.time.delay(100)
        index = random.randint(0, len(self.vole_sounds) - 1)
        self.vole_sounds[index].play()

class Main_Menu:
    def __init__(self, screen, game_state_manager):
        self.screen = screen
        self.game_state_manager = game_state_manager
        # Initialize the PlayButton with position and size for triangle
        self.play_button = PlayButton(SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT // 2 - 25, 100, self.start_game)
        self.quit_button = QuitButton(SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT // 2 +100, 100, 50, 'Quit', self.quit_game)
        pygame.mouse.set_visible(True)  # Make the mouse visible
        
        # Load background image
        self.background_image = pygame.image.load('./images/homescreen.png')  # Change the path to your image
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale it to fit the screen

        # Load font for title
        self.title_font = pygame.font.Font(None, 74)  # You can adjust the font size

    def draw(self):
        # Draw the background image
        self.screen.blit(self.background_image, (0, 0))
        
        # Draw the game title
        title_surface = self.title_font.render('Protect The Paddy Field', True, (0, 0, 0))  # Black text
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 3))  # Center the title
        self.screen.blit(title_surface, title_rect)  # Draw the title
        
        # Draw the play button
        self.play_button.draw(self.screen)     
        self.quit_button.draw(self.screen) 
		
    def start_game(self):
        self.game_state_manager.set_state('gameplay')  # Change state to gameplay
    def quit_game(self):
        self.game_state_manager.set_state('quit')

    def run(self):
        self.draw()
        pygame.mouse.set_visible(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state_manager.set_state('quit')
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.play_button.is_clicked(event.pos)
                    self.quit_button.is_clicked(event.pos)
class Game:
    def __init__(self):
        self.game_state_manager = Game_State_Manager('main_menu')
        pygame.init()
        # self.game_state_manager = Game_State_Manager('gameplay')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Protect The Paddy Field')
        pygame.display.set_icon(pygame.image.load('./images/rice.png'))
        self.clock = pygame.time.Clock() 
        self.game_play = Game_Play(self.screen, self.game_state_manager)
        self.main_menu = Main_Menu(self.screen, self.game_state_manager)
        self.game_over = Game_Over(self.screen, self.game_state_manager, self.game_play.score)
        self.states = {'gameplay':self.game_play, 'main_menu':self.main_menu, 'game_over': self.game_over}
        self.running = True
        self.background_image = pygame.image.load('./images/background.jpg')
        self.background_image = pygame.transform.scale(self.background_image, self.screen.get_size())
        

    # def run(self):
    #     while self.running:
    #         dt = self.clock.tick(60) / 1000 
    #         current_state = self.game_state_manager.get_state()
    #         if current_state == 'quit':
    #             self.running = False
    #         elif current_state == 'gameplay':
    #             self.states['gameplay'] = Game_Play(self.screen, self.game_state_manager)
    #             self.states['gameplay'].run(dt)
    #         elif current_state == 'game_over':
    #             score = self.states['gameplay'].score
    #             self.states['game_over'] = Game_Over(self.screen, self.game_state_manager, score)
    #             self.states['game_over'].run(dt)
    #         elif current_state == 'main_menu':
    #             self.states['main_menu'].run()
    #     pygame.quit()
    #     self.game_play = None
    #     self.main_menu = Main_Menu(self.screen, self.game_state_manager)
    #     self.states = {'main_menu': self.main_menu}

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000  # Calculate delta time
            if self.game_state_manager.get_state() == 'quit':
                self.running = False
            else:
                current_state = self.states[self.game_state_manager.get_state()]
                if isinstance(current_state, Main_Menu):
                    current_state.run()
                elif isinstance(current_state, Game_Play):
                    current_state.run(dt)
                elif isinstance(current_state, Game_Over):
                    print(self.states['gameplay'].score)
                    current_state.score = self.states['gameplay'].score
                    # self.states['game_over'] = Game_Over(self.screen, self.game_state_manager, score)
                    current_state.run(dt)

                # Check if we need to switch to gameplay
                if self.game_state_manager.get_state() == 'gameplay':
                    # Remove the old instance if it exists
                    if self.game_play is not None:
                        del self.game_play
                    
                    # Create a new instance of Game_Play
                    self.game_play = Game_Play(self.screen, self.game_state_manager)
                    self.states['gameplay'] = self.game_play  # Update the states dictionary

            pygame.display.update()

class Game_State_Manager:
    def __init__(self, current_state):
        self.current_state = current_state

    def set_state(self, current_state):
        self.current_state = current_state

    def get_state(self):
        return self.current_state

if __name__ == '__main__':
    game = Game()
    game.run()