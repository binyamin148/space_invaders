import pygame
from settings import *


class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        file_path = os.path.join(GRAPHICS_PATH, f'{color}.png')
        self.image = pygame.image.load(file_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.value = 100 if color == 'red' else 200 if color == 'green' else 300


    def update(self, direction):
        self.rect.x += direction * ALIEN_SPEED


class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        super().__init__()
        self.image = pygame.image.load(os.path.join(GRAPHICS_PATH, 'extra.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey(WHITE)
        
        if side == 'right':
            x = screen_width + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft=(x, 50))


    def update(self):
        self.rect.x += self.speed
