import pygame
from settings import *
from sprites.laser import Laser
from settings import SOUND_ENABLED, PLAYER_LASER_SPEED

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, screen_width, sound_manager):
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(GRAPHICS_PATH, 'chalal.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, PLAYER_SIZE)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = PLAYER_SPEED
        self.max_x_constraint = screen_width

        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = PLAYER_LASER_COOLDOWN
        self.lasers = pygame.sprite.Group()
        self.sound_manager = sound_manager


    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def constraint(self):
        self.rect.clamp_ip(pygame.Rect(0, 0, self.max_x_constraint, SCREEN_HEIGHT))


    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, PLAYER_LASER_SPEED, self.rect.bottom))
        if SOUND_ENABLED:
            self.sound_manager.play_sound('laser')

    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()
