import pygame
from word import *

    # hauteur 12
    # horizontale 23
    # start 12, 3
    # start2 4, 0
class BouleGame:
    def __init__(self, ):
        self.terrain = terrain
        self.largeur_fenetre = 1000
        self.hauteur_fenetre = 550
        self.couleur_fond = (255, 255, 255)
        self.pixels = 40
        self.vitesse_boule = 20

        pygame.init()
        self.fenetre = pygame.display.set_mode((self.largeur_fenetre, self.hauteur_fenetre))
        pygame.display.set_caption("Déplacement de boule")
        self.horloge = pygame.time.Clock()

        self.image_boule = pygame.image.load('Assets/alien.png')
        self.image_boule = pygame.transform.scale(self.image_boule, (self.pixels, self.pixels))

        self.image_mur = pygame.image.load('Assets/Armes/wals.png')
        self.image_mur = pygame.transform.scale(self.image_mur, (self.pixels, self.pixels))

        self.image_chemin = pygame.image.load('Assets/sable.jpg')
        self.image_chemin = pygame.transform.scale(self.image_chemin, (self.pixels, self.pixels))

        self.image_menu = pygame.image.load("Assets/Armes/Image 89 at frame 1copy .jpg")
        self.image_menu = pygame.transform.scale(self.image_menu, (self.pixels, self.pixels))
        self.pos_monstre = [11, 1]
        self.positions_visitees = []

    def est_position_valide(self, position):
        x, y = position
        return 0 <= x < len(self.terrain) and 0 <= y < len(self.terrain[0]) and self.terrain[x][y] == 0

    def deplacer(self):
        x, y = self.pos_monstre

        if x - 1 >= 0 and self.est_position_valide([x - 1, y]) and [x - 1, y] not in self.positions_visitees:
            self.pos_monstre = [x - 1, y]  # Déplacer vers le haut

        elif y + 1 < len(self.terrain[0]) and self.est_position_valide([x, y + 1]) and [x, y + 1] not in self.positions_visitees:
            self.pos_monstre = [x, y + 1]  # Déplacer vers la droite

        elif x + 1 < len(self.terrain) and self.est_position_valide([x + 1, y]) and [x + 1, y] not in self.positions_visitees:
            self.pos_monstre = [x + 1, y]  # Déplacer vers le bas

        elif y - 1 >= 0 and self.est_position_valide([x, y - 1]) and [x, y - 1] not in self.positions_visitees:
            self.pos_monstre = [x, y - 1]  # Déplacer vers la gauche

    def run(self):
        terminer = False
        while not terminer:
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    terminer = True

            self.deplacer()
            self.positions_visitees.append(self.pos_monstre)
            self.fenetre.fill(self.couleur_fond)

            for i in range(len(self.terrain)):
                for j in range(len(self.terrain[0])):
                    if self.terrain[i][j] == 1:
                        rect = pygame.Rect(j * self.pixels, i * self.pixels, self.pixels, self.pixels)
                        self.fenetre.blit(self.image_mur, rect)
                    elif self.terrain[i][j] == 0:
                        rect = pygame.Rect(j * self.pixels, i * self.pixels, self.pixels, self.pixels)
                        self.fenetre.blit(self.image_chemin, rect)
                    elif self.terrain[i][j] == 2:
                        rect = pygame.Rect(j * self.pixels, i * self.pixels, self.pixels, self.pixels)
                        self.fenetre.blit(self.image_menu, rect)

            self.fenetre.blit(self.image_boule, (self.pos_monstre[1] * self.pixels, self.pos_monstre[0] * self.pixels))

            pygame.display.flip()
            self.horloge.tick(self.vitesse_boule)

        pygame.quit()

game = BouleGame()
game.run()