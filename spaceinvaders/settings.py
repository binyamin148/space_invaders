import os

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PLAYER_SPEED = 5
PLAYER_SIZE = (100, 100)
PLAYER_LASER_COOLDOWN = 100

ALIEN_ROWS = 6
ALIEN_COLS = 8
ALIEN_X_DISTANCE = 60
ALIEN_Y_DISTANCE = 48
ALIEN_X_OFFSET = 70
ALIEN_Y_OFFSET = 100
ALIEN_SPEED = 1

PLAYER_LASER_SPEED = -10
ALIEN_LASER_SPEED = 6

OBSTACLE_AMOUNT = 4
OBSTACLE_BLOCK_SIZE = 8


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
GRAPHICS_PATH = os.path.join(BASE_PATH, 'graphics')
SOUNDS_PATH = os.path.join(BASE_PATH, 'sounds')

SOUND_ENABLED = True
MUSIC_VOLUME = 0.5
SFX_VOLUME = 1.0