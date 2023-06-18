import time

import pygame
import math
from src.componant.Projectille import Projectile
from src.Assets.const import *


class Arme:
    all_projectiles = pygame.sprite.Group()
    last_shot_time = 0
    shot_delay = 0  # Délai en secondes entre chaque lancement de projectile
    arme_en_tir = True
    projectile_delay = 1
    distance_min =150

    def __init__(self, position_x, position_y, image, types):

        self.type = types
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (72, 80)).convert()
        self.position_x = position_x
        self.position_y = position_y
        self.rect = self.image.get_rect(center=(position_x, position_y))
        self.position = (position_x, position_y)
        self.start = False
        self.is_placed = False
        self.angle = 0  # Angle de rotation initial
        self.rotated_image = self.image  # Image tournée
        self.all_projectilles = pygame.sprite.Group()
        self.cadenas_image = pygame.image.load(IMG_LOCK)
        self.cadenas_visible = True
        self.cout_arme = 25
        self.deverrouille = False
        self.check_arme = True
        self.is_selected = False
        self.selected = False
        self.direction = (0, 0)
        self.porte=50

    def draw_armes(self, window):
        if self.type=="arme_1":
            t=50
            window.blit(self.image, (self.position_x, self.position_y))
            if self.cadenas_visible:
                window.blit(self.cadenas_image, (self.position_x, self.position_y))
                police = pygame.font.Font(None, 30)
                texte_montant = police.render("{}".format(t), True, (255, 255, 255))
                window.blit(texte_montant, (self.rect.right +10, self.rect.top + 40))
        if self.type=="arme_2":
            t=80
            window.blit(self.image, (self.position_x, self.position_y))
            if self.cadenas_visible:
                window.blit(self.cadenas_image, (self.position_x, self.position_y))
                police = pygame.font.Font(None, 30)
                texte_montant = police.render("{}".format(t), True, (255, 255, 255))
                window.blit(texte_montant, (self.rect.right +10, self.rect.top + 40))
        if self.type=="arme_3":
            t=120
            window.blit(self.image, (self.position_x, self.position_y))
            if self.cadenas_visible:
                window.blit(self.cadenas_image, (self.position_x, self.position_y))
                police = pygame.font.Font(None, 30)
                texte_montant = police.render("{}".format(t), True, (255, 255, 255))
                window.blit(texte_montant, (self.rect.right +10, self.rect.top + 40))



    def draw_armess(self, is_placed, window):
        if is_placed:  # Vérifier si l'arme est placée
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            rotated_rect = rotated_image.get_rect(center=(self.position_x, self.position_y))
            window.blit(rotated_image, rotated_rect)
        else:
            window.blit(self.image, (self.position_x, self.position_y))

        if self.cadenas_visible:
            window.blit(self.cadenas_image, (self.position_x, self.position_y))

    def acheter(self, joueur):
        if joueur.argent >= self.cout_arme:
            joueur.argent -= self.cout_arme
            self.cadenas_visible = False

    def cliquer(self, joueur):
        if self.cadenas_visible and joueur.argent >= self.cout_arme:
            joueur.argent -= self.cout_arme
            self.cadenas_visible = False

    def is_clicked_armes(self, mouse_pos):
        rect = self.image.get_rect().move(self.position_x, self.position_y)
        return rect.collidepoint(mouse_pos)

    def resize_image(self, size):
        self.image = pygame.transform.scale(self.image, size)
        self.image.set_colorkey((0, 0, 0))

    def update_position(self, x, y):

        self.position_x = x
        self.position_y = y

    def type_arme(self, screen, pixels):
        if self.type == "arme_1":
            screen.blit(self.image, (self.position_x + pixels, self.position_y + pixels))

    @classmethod
    def detecter_monstres(cls, armes, monster_position, champ_vision ,screen):
        distance_min = 150
        cercle_size = 100
        for arme in armes:
            distance = math.sqrt(
                (arme.position_x - monster_position[0]) ** 2 + (arme.position_y - monster_position[1]) ** 2)

            if distance <= distance_min and distance <= champ_vision:
                pygame.draw.circle(screen, (255, 255, 255), (arme.position_x,arme.position_y), cercle_size, 1)
                cls.lancer_projectiles(arme.position_x, arme.position_y, monster_position,arme.type)

    @classmethod
    def lancer_projectiles(cls, position_x, position_y, target_position, type_arme):
        current_time = time.time()
        if current_time - cls.last_shot_time >= cls.projectile_delay:
            projectile_image = None
            if type_arme == "arme_1":
                projectile_image = pygame.image.load(WEAPON_RED_BULLET).convert_alpha()
                speed = 4
            elif type_arme == "arme_2":
                projectile_image = pygame.image.load(WEAPON_GREEN_BULLET).convert_alpha()
                speed = 6
            elif type_arme == "arme_3":
                projectile_image = pygame.image.load(WEAPON_BLUE_BULLET).convert_alpha()
                speed=8
            elif type_arme == "arme_1_plus":
                projectile_image = pygame.image.load(FIRE_BALL).convert_alpha()
                speed = 6
            elif type_arme =="arme_2_plus":
                projectile_image = pygame.image.load(EXPLOSION).convert_alpha()
                speed = 7
            elif type_arme == "arme_3_plus":
                 projectile_image = pygame.image.load(WEAPON_BLUE_BULLET).convert_alpha()
                 speed=10

            projectile = Projectile(position_x + 25, position_y - 3, target_position, projectile_image,speed)
            cls.all_projectiles.add(projectile)
            cls.last_shot_time = current_time

    @classmethod
    def lancer_projectiless(cls, position_x, position_y, target_position):
        projectile = Projectile(position_x + 25, position_y - 3, target_position)
        cls.all_projectiles.add(projectile)
