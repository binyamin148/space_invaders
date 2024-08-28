import pygame
import sys
from settings import *
from game import Game

class SpaceInvaders:
    def __init__(self):
        pygame.init()
        if SOUND_ENABLED:
            pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.game = Game(self.screen)
        
        self.bg_image = pygame.image.load(os.path.join(GRAPHICS_PATH, 'bg.jpg'))
        self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.ALIENLASER = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ALIENLASER, 800)
        
        

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if SOUND_ENABLED:
                        self.game.sound_manager.stop_background_music()
                    pygame.quit()
                    sys.exit()
                if event.type == self.ALIENLASER:
                    self.game.alien_shoot()

            self.screen.fill(BLACK)
            self.screen.blit(self.bg_image, (0, 0))

            self.game.run()

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = SpaceInvaders()
    game.run()