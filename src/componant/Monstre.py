from collections import deque
from datetime import time
from random import random

import pygame
from src.Assets.const import *


class Piece:
    pieces_gagnees = []

    def __init__(self, position_x, position_y, image):
        self.position_x = position_x
        self.position_y = position_y
        self.image = image
        self.animation_duree = 0
        self.animation_speed = 5

    def afficher_animation(self, screen):
        self.position_y -= self.animation_speed
        self.animation_duree += 1

        self.image = pygame.transform.scale(self.image, (10, 10))

        screen.blit(self.image, (self.position_x + 50, self.position_y + 60))

        if self.animation_duree >= 2:
            if self in Piece.pieces_gagnees:
                Piece.pieces_gagnees.remove(self)


class Monstre(pygame.sprite.Sprite):
    pieces_gagnees = []
    # Abdoulaye
    def __init__(self, positionX, positionY, defense = 0):
        super().__init__()
        self.image_monstre = pygame.image.load(MONSTER_1)
        self.image_monstre = pygame.transform.scale(self.image_monstre, (35, 30))
        self.positionX = positionX
        self.positionY = positionY
        self.rect = self.image_monstre.get_rect()
        self.rect.x = self.positionX
        self.rect.y = self.positionY
        self.rect.width = self.image_monstre.get_width() - 8
        self.rect.center = (self.positionX, self.positionY)
        self.rect.height = self.image_monstre.get_height() - 2
        self.vitesse = 3
        self.health = 2
        self.direction_x = 0
        self.direction_y = 0
        self.nbr_vie = 50
        self.nbr_vie_max = 50
        self.degat = 10
        self.positions_visitees = set()
        self.position_monstre = [self.positionX, self.positionY]
        self.defense = defense
        self.current_position_index = 0


    # Victor
    # def __init__(self, image_monstre, positionX, positionY, vitesse):
    #     self.image_monstre = image_monstre
    #     self.positionX = positionX
    #     self.positionY = positionY
    #     self.vitesse = vitesse
    #     self.rect = self.image_monstre.get_rect()
    #     self.current_position_index = 0


    # Abdoulaye
    # @classmethod
    # def detecter_collision_monstres(cls, monstres, projectiles, Map):

    #     for monstre in monstres:
    #         for projectile in projectiles:
    #             if monstre.rect.colliderect(projectile.rect):
    #                 # Collision détectée entre le monstre et le projectile
    #                 monstre.nbr_vie -= 5
    #                 projectiles.remove(projectile)  # Supprimer le projectile lorsqu'il touche le monstre
    #                 if monstre.nbr_vie <= 0:
    #                     cls.gagner_piece(monstre.positionX, monstre.positionY)  # Gagner une pièce
    #                     monstres.remove(monstre)
    #                     Map.argent += 5
    @classmethod
    def detecter_collision_monstres(cls, monstres, projectiles, Map):
        for monstre in monstres:
            for projectile in projectiles:
                if monstre.rect.colliderect(projectile.rect):
                    # Collision détectée entre le monstre et le projectile
                    degats = 5
                    if monstre.defense > 0:
                        degats -= monstre.defense
                        degats = max(0, degats)  # Les dégâts ne peuvent pas être négatifs
                    
                    monstre.nbr_vie -= degats
                    projectiles.remove(projectile)  # Supprimer le projectile lorsqu'il touche le monstre
                    
                    if monstre.nbr_vie <= 0:
                        cls.gagner_piece(monstre.positionX, monstre.positionY)  # Gagner une pièce
                        monstres.remove(monstre)
                        Map.argent += 5


    def position_depart(self):
        self.positionX = 84
        self.positionY = 480

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
        text = font.render(message, True,(255, 255, 255))  # Créer une surface de texte avec le message et la couleur blanche
        text_rect = text.get_rect(center=self.rect.center)  # Obtenir le rectangle du texte centré sur le monstre
        screen.blit(text, text_rect)  # Afficher le texte à l'écran

    def move(self):

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.direction_y = -1
                    self.positionY += self.direction_y * 3
                elif event.key == pygame.K_DOWN:
                    self.direction_y = 1
                    self.positionY += self.direction_y * 3
                elif event.key == pygame.K_LEFT:
                    self.direction_x = -1
                    self.positionX += self.direction_x * 5
                elif event.key == pygame.K_RIGHT:
                    self.direction_x = 1
                    self.positionX += self.direction_x * 3

        print("{0},{1}".format(self.positionX, self.positionY))

    # def draw_monstre_map_1(self, screen, pixels):
    # # si map 1 si map 2

    #     if self.image_monstre is not None:
    #         screen.blit(self.image_monstre, (self.positionX + pixels, self.positionY + pixels))
    #         pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
    #         positions = [(84, 324), (564, 324), (564, 42), (165, 42), (165, -78)]
    #         target_position = positions[self.current_position_index]
    #         target_x, target_y = target_position

    #         if self.positionX < target_x:
    #             self.positionX += self.vitesse
    #         elif self.positionX > target_x:
    #             self.positionX -= self.vitesse

    #         if self.positionY < target_y:
    #             self.positionY += self.vitesse
    #         elif self.positionY > target_y:
    #             self.positionY -= self.vitesse

    #         if self.positionX == target_x and self.positionY == target_y:
    #             self.current_position_index += 1
    #             if self.current_position_index >= len(positions):
    #                 # Arrête le monstre après avoir dépassé la dernière position
    #                 self.current_position_index = len(positions) - 1
    # ---------------------- TEST ----------------------
    def draw_monstre_map_1(self, screen, pixels, current_map):
    # si map 1 si map 2

        if self.image_monstre is not None:
            screen.blit(self.image_monstre, (self.positionX + pixels, self.positionY + pixels))
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
            positions_map1 = [(84, 324), (564, 324), (564, 42), (165, 42), (165, -78)]
            positions_map2 = [(84, 327),(123, 327),(123, 288),(168, 288),(168, 165),(489, 165),(489, 84),(444, 84),(444, -78)]
            positions_map3 = [(84, 327),(123, 327),(123, 288),(489, 288),(489, 168),(165, 168),(165, -78)]


            if current_map == 1:
                positions = positions_map1
            elif current_map == 2:
                positions = positions_map2
            elif current_map == 3:
                positions = positions_map3
            else:
                raise ValueError("Invalid map number")

            target_position = positions[self.current_position_index]
            target_x, target_y = target_position

            if self.positionX < target_x:
                self.positionX += self.vitesse
            elif self.positionX > target_x:
                self.positionX -= self.vitesse

            if self.positionY < target_y:
                self.positionY += self.vitesse
            elif self.positionY > target_y:
                self.positionY -= self.vitesse

            if self.positionX == target_x and self.positionY == target_y:
                self.current_position_index += 1
                if self.current_position_index >= len(positions):
                    # Arrête le monstre après avoir dépassé la dernière position
                    self.current_position_index = len(positions) - 1
            
 
    def draw_monstre_map_2(self, screen, pixels):
    # si map 1 si map 2

        if self.image_monstre is not None:
            screen.blit(self.image_monstre, (self.positionX + pixels, self.positionY + pixels))
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
            positions2 = [(84, 327),(123, 327),(123, 288),(168, 288),(168, 165),(489, 165),(489, 84),(444, 84),(444, -78)]
            target_position = positions2[self.current_position_index]
            target_x, target_y = target_position

            if self.positionX < target_x:
                self.positionX += self.vitesse
            elif self.positionX > target_x:
                self.positionX -= self.vitesse

            if self.positionY < target_y:
                self.positionY += self.vitesse
            elif self.positionY > target_y:
                self.positionY -= self.vitesse

            if self.positionX == target_x and self.positionY == target_y:
                self.current_position_index += 1
                if self.current_position_index >= len(positions2):
                    # Arrête le monstre après avoir dépassé la dernière position
                    self.current_position_index = len(positions2) - 1

    def draw_monstre_map_3(self, screen, pixels):
    # si map 1 si map 2

        if self.image_monstre is not None:
            screen.blit(self.image_monstre, (self.positionX + pixels, self.positionY + pixels))
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
            positions3 = [(84, 327),(123, 327),(123, 288),(489, 288),(489, 168),(165, 168),(165, -78)]
            target_position = positions3[self.current_position_index]
            target_x, target_y = target_position

            if self.positionX < target_x:
                self.positionX += self.vitesse
            elif self.positionX > target_x:
                self.positionX -= self.vitesse

            if self.positionY < target_y:
                self.positionY += self.vitesse
            elif self.positionY > target_y:
                self.positionY -= self.vitesse

            if self.positionX == target_x and self.positionY == target_y:
                self.current_position_index += 1
                if self.current_position_index >= len(positions3):
                    # Arrête le monstre après avoir dépassé la dernière position
                    self.current_position_index = len(positions3) - 1


    def update_monstre(self, screen, pixels):
        screen.blit(self.image_monstre, (self.positionX + pixels, self.positionY + pixels))

    def getPositionY(self):
        print("Position X et Y: {0},{1}".format(self.positionX, self.positionY))
        # print("Taille {0}".format(self.image_monstre.get_size()))

    def update_projectille(self, projectiles):
        self.detecter_collision_projectile(projectiles)

    def remove(self):
        # Ajoutez ici la logique pour faire disparaître le monstre
        # Par exemple, vous pouvez le rendre invisible en définissant son attribut image à None :
        print(self.rect)

    def update_velocite_rect(self):
        self.rect.x = self.positionX + 45
        self.rect.y = self.positionY + 42

    @classmethod
    def gagner_piece(cls, position_x, position_y):
        piece_image = pygame.image.load(COIN).convert_alpha()
        piece = Piece(position_x, position_y, piece_image)
        cls.pieces_gagnees.append(piece)

    @classmethod
    def afficher_pieces_gagnees(cls, screen):
        for piece in cls.pieces_gagnees:
            piece.afficher_animation(screen)
            if piece.animation_duree >= 10:
                cls.pieces_gagnees.remove(piece)  # Supprimer la pièce de la liste lorsque l'animation est terminée
