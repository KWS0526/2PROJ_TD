import random

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
    augmentation_vie_effectuee = False
    images_monstre = {MONSTER_1: "type_1",
                      MONSTER_2: "type_2",
                      MONSTER_3: "type_3",
                      MONSTER_5: "type_5",
                      MONSTER_6: "type_6",
                      MONSTER_7: "type_7",
                      MONSTER_8: "type_8"
                      }

    # Abdoulaye
    def __init__(self, positionX, positionY, defense=0):
        super().__init__()

        chemin_image_monstre = random.choice(list(Monstre.images_monstre.keys()))
        self.image_monstre = pygame.image.load(chemin_image_monstre)
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
        self.type = Monstre.images_monstre[chemin_image_monstre]

    def set_image_monstre_aleatoire(self):
        # Dictionnaire d'images pour chaque type de monstre
        images_monstres = {
            "monstre1": MONSTER_1,
            "monstre2": MONSTER_2,
            "monstre3": MONSTER_3,
            "monstre4": MONSTER_5,
            "monster5": MONSTER_6,
            "monster6": MONSTER_7,
            "monster7": MONSTER_8
            # Ajoutez d'autres types de monstres et leurs chemins d'accès aux images ici
        }

        # Sélection aléatoire d'un type de monstre
        type_monstre = random.choice(list(images_monstres.keys()))
        image_monstre = images_monstres[type_monstre]

        self.image_monstre = pygame.image.load(image_monstre)

    @classmethod
    def detecter_collision_monstres(cls, monstres, projectiles, Map):

        for monstre in monstres:
            for projectile in projectiles:
                if monstre.rect.colliderect(projectile.rect):
                    # Collision détectée entre le monstre et le projectile
                    degats = 5
                    if monstre.defense > 0:
                        degats -= monstre.defense
                        degats = max(0, degats)

                    if monstre.type == "type_1":
                        degats = 10
                        monstre.defense=1
                        monstre.nbr_vie=5
                        monstre.degat=10
                    if monstre.type == "type_2":
                        degats = 10
                        monstre.nbr_vie=5
                        monstre.degat=10
                    if monstre.type == "type_4":
                        degats = 30
                        monstre.nbr_vie=5
                    if monstre.type == "type_5":
                        degats = 50
                        monstre.nbr_vie=5
                        monstre.degat=1
                    if monstre.type == "type_6":
                        degats = 15
                        monstre.defense=1
                        monstre.nbr_vie=5
                        monstre.degat=15
                    if monstre.type == "type_7":
                        degats = 50
                        monstre.defense=0
                        monstre.nbr_vie=5
                        monstre.degat=1
                    if monstre.type == "type_8":
                        degats = 50
                        monstre.nbr_vie=1
                        monstre.degat=1

                    monstre.nbr_vie -= degats
                    projectiles.remove(projectile)  # Supprimer le projectile lorsqu'il touche le monstre

                    if monstre.nbr_vie <= 0:
                        cls.gagner_piece(monstre.positionX, monstre.positionY)  # Gagner une pièce
                        monstres.remove(monstre)
                        Map.argent += 5

        if len(monstres) == 3 and not cls.augmentation_vie_effectuee:
            for monstre in monstres:
                monstre.nbr_vie += 5

            cls.augmentation_vie_effectuee = True

    def update_bar_de_vie(self, surface):
        bar_color = (231, 52, 14)
        bar_width = 50  # Largeur fixe de la barre de vie
        bar_height = 3  # Hauteur de la barre de vie
        couleur_arriere_plan = (60, 63, 60)
        arriere_plan_width = 50  # Largeur fixe de l'arrière-plan de la barre
        arriere_plan_height = 3  # Hauteur de l'arrière-plan de la barre

        pourcentage_vie_restante = self.nbr_vie / self.nbr_vie_max
        vie_restante_width = int(bar_width * pourcentage_vie_restante)

        position_arriere_plan = [self.positionX + 30, self.positionY + 36, arriere_plan_width, arriere_plan_height]
        position = [self.positionX + 30, self.positionY + 36, vie_restante_width, bar_height]

        pygame.draw.rect(surface, couleur_arriere_plan, position_arriere_plan)
        pygame.draw.rect(surface, bar_color, position)

    def show_message(self, screen, message):
        font = pygame.font.Font(None, 24)  # Définir la police et la taille du texte
        text = font.render(message, True,
                           (255, 255, 255))  # Créer une surface de texte avec le message et la couleur blanche
        text_rect = text.get_rect(center=self.rect.center)  # Obtenir le rectangle du texte centré sur le monstre
        screen.blit(text, text_rect)  # Afficher le texte à l'écran

    def draw_monstre(self, screen, pixels, current_map):

        if self.image_monstre is not None:
            screen.blit(self.image_monstre, (self.positionX + pixels, self.positionY + pixels))
            positions_map1 = [(84, 324), (564, 324), (564, 42), (165, 42), (165, -78)]
            positions_map2 = [(84, 327), (123, 327), (123, 288), (168, 288), (168, 165), (489, 165), (489, 84),(444, 84), (444, -78)]
            positions_map3 = [(84, 327), (123, 327), (123, 288), (489, 288), (489, 168), (165, 168), (165, -78)]

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
