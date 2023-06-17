import pygame
import random

class Sound:
    def __init__(self, musiques):
        pygame.mixer.init()
        self.musiques = musiques
        self.charger = False
        self.play = False
        self.volume = 0.2

        self.load_sound()
        self.play_sound()

    def load_sound(self):
        musique_aleatoire = random.choice(self.musiques)
        pygame.mixer.music.load(musique_aleatoire)
        self.charger = True

    def play_sound(self, loop=-1):
        self.charger = True
        if not self.charger:
            self.load_sound()
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(loop)
        self.play = True

    def stop_sound(self):
        pygame.mixer.music.stop()
        self.play = False
