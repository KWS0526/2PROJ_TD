import pygame
from src.componant.Monstre import Monstre

class Wave_monster:
    def __init__(self):
        self.vagues_de_monstres = []

    def generer_vagues(self, ecart_y, nb_vagues, nb_monstres_par_vague, position_y_initiale):
        position_y = position_y_initiale

        for i in range(nb_vagues):
            vague = [Monstre(84, position_y + (ecart_y * j)) for j in range(nb_monstres_par_vague)]
            self.vagues_de_monstres.append(vague)
            position_y += ecart_y

