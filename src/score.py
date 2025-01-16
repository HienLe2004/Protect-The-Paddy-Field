from setting import *
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
