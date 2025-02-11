from setting import *

class Game_Clock(object):
    def __init__(self):
        self.duration = 10  # Tổng thời gian trò chơi (giây)
        self.start_ticks = pygame.time.get_ticks()  # Lưu thời điểm bắt đầu
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.text = self.font.render(str(self.duration), True, (0, 0, 0))
        self.rect = self.text.get_rect(midtop=(SCREEN_WIDTH / 2, 10))
        self.time_up = False

    def draw(self, surf):
        surf.blit(self.text, self.rect)
    
    def update(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_ticks) / 1000  # Tính thời gian đã trôi qua (giây)
        remaining_time = max(0, self.duration - int(elapsed_time))
        
        if remaining_time == 0:
            #print("end")
            self.time_up = True
            
        self.text = self.font.render(str(remaining_time), True, (0, 0, 0))
        self.rect = self.text.get_rect(midtop=(SCREEN_WIDTH / 2, 10))

