import math

import pygame
from pygame.sprite import Sprite
from src.Assets.const import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_position_x, start_position_y, target_position, image, speed=4):
        super().__init__()
        self.start_position_x = start_position_x
        self.start_position_y = start_position_y
        self.target_position = target_position
        self.image = image

        # Redimensionne l'image du projectile à une taille de 10x10 pixels
        self.image = pygame.transform.scale(self.image, (10, 10)).convert_alpha()
        self.rect = self.image.get_rect(center=(start_position_x, start_position_y))
        self.speed = speed

        # Calcul des distances et directions entre la position de départ et la position cible
        self.dx = target_position[0] - start_position_x
        self.dy = target_position[1] - start_position_y
        self.distance = math.sqrt(self.dx ** 2 + self.dy ** 2)

        if self.distance != 0:
            # Calcul des directions normalisées du projectile
            self.direction_x = self.dx / self.distance
            self.direction_y = self.dy / self.distance
        else:
            self.direction_x = 0
            self.direction_y = 0

    def update(self):
        # Mise à jour de la position du projectile en fonction de sa direction et de sa vitesse
        self.start_position_x += self.direction_x * self.speed
        self.start_position_y += self.direction_y * self.speed
        self.rect.center = (self.start_position_x, self.start_position_y)

    def draw(self, screen):
        # Dessine le projectile sur l'écran
        screen.blit(self.image, self.rect)

    def detecter_collision_monstres(self, monstres):
        for monstre in monstres:
            if self.rect.colliderect(monstre.rect):
                degats = 50
                if monstre.defense > 0:
                    # Réduction des dégâts en fonction de la défense du monstre
                    reduction_degats = int(degats * monstre.defense / 100)
                    degats -= reduction_degats

                # Inflige des dégâts au monstre et supprime le projectile
                monstre.nbr_vie -= degats
                self.kill()
                print("Projectile touché un monstre")

                if monstre.nbr_vie <= 0:
                    # Supprime le monstre si ses points de vie atteignent zéro ou moins
                    print(monstre.nbr_vie)
                    monstre.kill()
