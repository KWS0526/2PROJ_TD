import pygame

class Sound:
    def __init__(self, nom_musique):
        pygame.mixer.init()
        self.nom_musique = nom_musique
        self.charger = False
        self.play = False
        self.volume = 0.1

        self.load_sound()
        self.play_sound()

    def load_sound(self):
        pygame.mixer.music.load(self.nom_musique)
        self.charger = True

    def play_sound(self, loop=-1):
        if not self.charger:
            self.load_sound()
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(loop)
        self.play = True

    def stop_sound(self):
        pygame.mixer.music.stop()
        self.play = False
