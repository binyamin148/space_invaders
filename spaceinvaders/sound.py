import pygame
from settings import SOUNDS_PATH
import os

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            'laser': pygame.mixer.Sound(os.path.join(SOUNDS_PATH, 'laser.wav')),
            'explosion': pygame.mixer.Sound(os.path.join(SOUNDS_PATH, 'explosion.wav')),
        }
        self.background_music = os.path.join(SOUNDS_PATH, 'background_music.wav')

    def play_sound(self, sound_name):
        self.sounds[sound_name].play()

    def play_background_music(self):
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely

    def stop_background_music(self):
        pygame.mixer.music.stop()