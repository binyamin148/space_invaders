import pygame
import random
import sys
from settings import *
from sprites.player import Player
from sprites.alien import Alien, Extra
from sprites.laser import Laser
from sprites.obstacle import Block, shape
from sound import SoundManager


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.sound_manager = SoundManager()
        if SOUND_ENABLED:
            self.sound_manager.play_background_music()
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            for sound in self.sound_manager.sounds.values():
                sound.set_volume(SFX_VOLUME)
        self.player = pygame.sprite.GroupSingle(Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT), SCREEN_WIDTH, self.sound_manager))
        self.lives = 3
        self.live_surf = pygame.image.load(os.path.join(GRAPHICS_PATH, 'chalal.png')).convert_alpha()
        self.live_surf = pygame.transform.scale(self.live_surf, (100, 100))
        self.live_surf.set_colorkey(WHITE)
        self.live_x_start_pos = SCREEN_WIDTH - (self.live_surf.get_size()[0] * 3 + 20)

        self.blocks = pygame.sprite.Group()
        self.create_multiple_obstacles()

        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup()
        self.alien_direction = 1
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = random.randint(40, 80)

        self.score = 0
        self.font = pygame.font.Font(os.path.join(GRAPHICS_PATH, 'Pixeled.ttf'), 20)
        
        

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * OBSTACLE_BLOCK_SIZE + offset_x
                    y = y_start + row_index * OBSTACLE_BLOCK_SIZE
                    block = Block(OBSTACLE_BLOCK_SIZE, WHITE, x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self):
        obstacle_x_positions = [num * (SCREEN_WIDTH / OBSTACLE_AMOUNT) for num in range(OBSTACLE_AMOUNT)]
        for offset_x in obstacle_x_positions:
            self.create_obstacle(SCREEN_WIDTH / 10, 480, offset_x)

    def alien_setup(self):
        for row_index in range(ALIEN_ROWS):
            for col_index in range(ALIEN_COLS):
                x = col_index * ALIEN_X_DISTANCE + ALIEN_X_OFFSET
                y = row_index * ALIEN_Y_DISTANCE + ALIEN_Y_OFFSET
                color = 'yellow' if row_index == 0 else 'green' if 1 <= row_index <= 2 else 'red'
                alien_sprite = Alien(color, x, y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        for alien in self.aliens.sprites():
            if alien.rect.right >= SCREEN_WIDTH or alien.rect.left <= 0:
                self.alien_direction *= -1
                self.alien_move_down(2)
                break

    def alien_move_down(self, distance):
        for alien in self.aliens.sprites():
            alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = random.choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, ALIEN_LASER_SPEED, SCREEN_HEIGHT)
            self.alien_lasers.add(laser_sprite)

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(random.choice(['right', 'left']), SCREEN_WIDTH))
            self.extra_spawn_time = random.randint(400, 800)

    def collision_checks(self):
        # Player lasers
        for laser in self.player.sprite.lasers:
            if pygame.sprite.spritecollide(laser, self.blocks, True):
                laser.kill()
                if SOUND_ENABLED:
                    self.sound_manager.play_sound('explosion')

            aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
            if aliens_hit:
                for alien in aliens_hit:
                    self.score += alien.value
                laser.kill()
                if SOUND_ENABLED:
                    self.sound_manager.play_sound('explosion')

            if pygame.sprite.spritecollide(laser, self.extra, True):
                self.score += 500
                laser.kill()
                if SOUND_ENABLED:
                    self.sound_manager.play_sound('explosion')

        # Alien lasers
        for laser in self.alien_lasers:
            if pygame.sprite.spritecollide(laser, self.blocks, True):
                laser.kill()

            if pygame.sprite.spritecollide(laser, self.player, False):
                laser.kill()
                self.lives -= 1

        # Aliens
        for alien in self.aliens:
            pygame.sprite.spritecollide(alien, self.blocks, True)
            if pygame.sprite.spritecollide(alien, self.player, False):
                self.lives = 0

    def display_lives(self):
        for live in range(self.lives):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            self.screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft=(10, -10))
        self.screen.blit(score_surf, score_rect)

    def victory_message(self):
        if not self.aliens.sprites():
            victory_surf = self.font.render('You won', False, 'white')
            victory_rect = victory_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            self.screen.blit(victory_surf, victory_rect)
            pygame.display.update()
            pygame.time.wait(5000)
            pygame.quit()
            sys.exit()

    def loss_message(self):
        if self.lives <= 0:
            loss_surf = self.font.render('Game over', True, 'white')
            loss_rect = loss_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            self.screen.blit(loss_surf, loss_rect)
            pygame.display.update()
            pygame.time.wait(5000)
            pygame.quit()
            sys.exit()

    def run(self):
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_lasers.update()
        self.extra.update()

        self.alien_position_checker()
        self.extra_alien_timer()
        self.collision_checks()

        self.player.sprite.lasers.draw(self.screen)
        self.player.draw(self.screen)
        self.blocks.draw(self.screen)
        self.aliens.draw(self.screen)
        self.alien_lasers.draw(self.screen)
        self.extra.draw(self.screen)
        self.display_lives()
        self.display_score()
        self.victory_message()
        self.loss_message()