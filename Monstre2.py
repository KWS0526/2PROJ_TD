from collections import deque
from datetime import time
from random import random

import pygame


class Monstre(pygame.sprite.Sprite):
    def __init__(self, positionX, positionY):
        super().__init__()
        self.image_monstre = pygame.image.load("Assets/Monsters/Turtle_monster.png")
        self.image_monstre = pygame.transform.scale(
           self.image_monstre, (35, 30))
        self.positionX = positionX
        self.positionY = positionY
        self.rect = self.image_monstre.get_rect()
        self.rect.x = self.positionX
        self.rect.y = self.positionY

        self.rect.width = self.image_monstre.get_width()-10
        self.rect.center = (self.positionX, self.positionY)

        self.rect.height = self.image_monstre.get_height()-2
        self.vitesse = 3
        self.health = 2
        self.direction_x = 0
        self.direction_y = 0
        self.nbr_vie = 50
        self.nbr_vie_max = 50
        self.degat = 25
        # self.positions_visitees = set()
        self.position_monstre = [self.positionX, self.positionY]
        self.positions_visitees = []

    @classmethod
    def detecter_collision_monstres(cls, monstres, projectiles, Map):

        for monstre in monstres:
            for projectile in projectiles:
                if monstre.rect.colliderect(projectile.rect):
                    # Collision détectée entre le monstre et le projectile
                    monstre.nbr_vie -= 5
                    projectiles.remove(projectile)  # Supprimer le projectile lorsqu'il touche le monstre
                    print("Monstre touché !")

                    if monstre.nbr_vie <= 0:
                        monstres.remove(monstre)
                        Map.argent +=20

    def update_bar_de_vie(self, surface):
        # j'ai defini un code couleurs rouge qui va etre au dessus du monstre qui etre son niveau de vie
        bar_color = (231, 52, 14)
        # la position va permetrre le niveaux de vie se deplace avec le monstre
        position = [self.positionX + 30, self.positionY + 36, self.nbr_vie, 3]
        # couleur de l'arriere plan qui va permettre devoir si le monstre a subit un degat
        couleur_arriere_plan = (60, 63, 60)
        # la position de l'arriere plan

        position_arriere_plan = [self.positionX + 30, self.positionY + 36, self.nbr_vie_max, 3]
        pygame.draw.rect(surface, couleur_arriere_plan, position_arriere_plan)
        pygame.draw.rect(surface, bar_color, position)

    def show_message(self, screen, message):
        font = pygame.font.Font(None, 24)  # Définir la police et la taille du texte
        text = font.render(message, True,
                           (255, 255, 255))  # Créer une surface de texte avec le message et la couleur blanche
        text_rect = text.get_rect(center=self.rect.center)  # Obtenir le rectangle du texte centré sur le monstre
        screen.blit(text, text_rect)  # Afficher le texte à l'écran

    def est_position_valide(self, position, world):
        x, y = position
        return 0 <= x < len(world) and 0 <= y < len(world[0]) and world[x][y] == 0

    def deplacer(self, world):
        x, y = self.position_monstre

        if x - 1 >= 0 and self.est_position_valide([x - 1, y], world) and [x - 1, y] not in self.positions_visitees:
            self.position_monstre = [x - 1, y]  # Déplacer vers le haut

        elif y + 1 < len(world[0]) and self.est_position_valide([x, y + 1], world) and [x, y + 1] not in self.positions_visitees:
            self.position_monstre = [x, y + 1]  # Déplacer vers la droite

        elif x + 1 < len(world) and self.est_position_valide([x + 1, y], world) and [x + 1, y] not in self.positions_visitees:
            self.position_monstre = [x + 1, y]  # Déplacer vers le bas

        elif y - 1 >= 0 and self.est_position_valide([x, y - 1], world) and [x, y - 1] not in self.positions_visitees:
            self.position_monstre = [x, y - 1]  # Déplacer vers la gauche

