import math

import pygame
import time
import os

from src.Assets.const import *
from src.componant.MenuMap import MenuGame
from src.componant.Projectille import Projectile
from src.componant.Sound import Sound
from src.componant.button import Button
from src.componant.Monstre2 import Monstre
from src.componant.Vie import Vie
from src.componant.Armes import Arme
from src.componant.Cartes import Carte
from src.componant.AfficheurTexte import AfficheurTexte
from src.componant.world import *


class Map:
    def __init__(self):
        # Pour lancer notre application en boucle
        self.selected_tower = None
        self.running = True
        # titre de notre jeu
        pygame.display.set_caption("Tower Defense")
        repertoire_actuel = os.getcwd()
        print("Répertoire de travail actuel :", repertoire_actuel)
        # on récupère notre matrix que l'on stocke sur un variable
        self.world = world
        # Définir la taille de la matrice et des carrés
        self.matrix_width = len(self.world[0])
        self.matrix_height = len(self.world)

        # la taille de chaque cellule dans le screen qu'on met  en pixels
        self.pixels = 40
        # Définir la taille de la fenêtre en fonction de notre matrice
        self.window_width = self.matrix_width * self.pixels
        self.window_height = self.matrix_height * self.pixels
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        self.background = pygame.image.load(BG_SABLE)
        self.background = pygame.transform.scale(self.background, (self.window_width, self.window_height))
        # definir l'image de faire de notre Menu

        self.Fond_Menu = pygame.image.load(FOND_MENU)
        self.Fond_Map = pygame.image.load(FOND_MAP)
        # instanciation de mon menu
        self.mes_button = {
            "button_Menu": Button(500, 100,BUTTON_MENU),
            "button_NewGame": Button(380, 270,NEW_GAME),
            "button_Options": Button(620, 270,OPTION),
            "button_Quitt": Button(500, 400,QUIT),
            "button_SousMenuMusique": Button(400, 200,MUSIQUE_NOTE),
            "button_SousMenuStopMusique": Button(620, 200,DECLINE),
            "button_SousMenuAudio": Button(400, 250,MUSIQUE_NOTE),
            "button_SousMenuStopAudio": Button(620, 250,DECLINE),
            "button_Retour": Button(520, 360,BACK)
        }
        self.cartes = {
            "carte_1": Carte(170, 270, CARTE_1),
            "carte_2": Carte(480, 270, CARTE_2),
            "carte_3": Carte(790, 270, CARTE_3),
            "retour": Carte(900, 300, RETOUR)
        }
        self.text = {
            "text_easy": AfficheurTexte("Facile", 150, 140, (123,104,238)),
            "text_medium": AfficheurTexte("Moyen", 430, 140, (123,104,238)),
            "text.difficile": AfficheurTexte("Difficile", 750, 140, (123,104,238)),
            "game_over": AfficheurTexte("Game Over", 400, 400, (199, 0, 57))
        }
        self.etat_button_options = "normal"
        self.etat = "menu"
        self.en_pause = "play"
        # instancier musiqueS
        self.sound = Sound("Musique/1.mp3")
        self.vie_joueur = Vie()
        # self.armes = {
        #    "arme_1": Arme(715, 40, "src/Assets/Armes/arme.png", "arme_1")
        # }
        self.mes_armess = [
            Arme(715, 40, ARME_1, "arme_1"),
            Arme(820, 40, ARME_2, "arme_2")
            # Ajoutez plus d'armes disponibles avec leurs positions
        ]
        self.mes_armes = []
        self.monstre_positions = []

        # self.vagues_de_monstres = [
        #   [Monstre(84, 480), Monstre(84, 552), Monstre(84, 624)],
        #  [Monstre(84, 480), Monstre(84, 552), Monstre(84, 624)]
        # ]
        self.vagues_de_monstres = []

        self.monstres_vague_actuelle = 0
        self.vague_actuelle = 0
        self.position_prochaine_vague = 165
        self.vague_affichee = False
        self.menu_map_screen = MenuGame(self)
        self.click = ""
        self.towers = []
        self.placing_tower = False
        self.selected_weapon = None
        self.argent = 200
        self.arme_placee_recente = True
        self.click_counter = 0
        self.initial_image_clicked = False
        self.arme_initiale = None
        self.type_arme = ""
        self.prix_arme_definie = None

        #---------------------------------
        self.vitesse_monstre = 25
        self.horloge = pygame.time.Clock()

        self.image_monstre = pygame.image.load(IMAGE_MONSTRE)
        self.image_monstre = pygame.transform.scale(self.image_monstre, (self.pixels, self.pixels))

        self.image_mur = pygame.image.load(IMG_MUR)
        self.image_mur = pygame.transform.scale(self.image_mur, (self.pixels, self.pixels))

        self.image_chemin = pygame.image.load(IMG_SABLE)
        self.image_chemin = pygame.transform.scale(self.image_chemin, (self.pixels, self.pixels))

        self.image_menu = pygame.image.load(IMG_ARME)
        self.image_menu = pygame.transform.scale(self.image_menu, (self.pixels, self.pixels))

    def waves(self, world, waves = 30):
        for i in range(len(world)):
            for j in range(len(world[0])):
                if world[i][j] == 5:
                    start = [i, j]

        for i in range(waves):
            vague = [Monstre(start[0], start[1]) for _ in range(10 + 2*i)]  # Coordonnées des monstres de la vague i
            self.vagues_de_monstres.append(vague)
    
    def draw(self):
        # Afficher les armes disponibles
        for armes in self.mes_armess:
            armes.draw_armes(self.screen)

        # Dessiner les tours placées
        for tower in self.towers:
            tower.draw_armess(self.placing_tower, self.screen)

        # pygame.display.update()

    def verifier_le_click_sur_quel_image(self, world):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if not self.initial_image_clicked:
                    for arme in self.mes_armess:
                        # Vérifier les conditions de clic sur l'image initiale
                        if arme.is_clicked_armes((x, y)):
                            arme.cliquer(self)
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
                            self.type_arme = arme.type
                            self.initial_image_clicked = True
                            self.prix_arme_definie = arme.cout_arme

                else:
                    if self.argent >= self.prix_arme_definie:
                        row = y // self.pixels
                        col = x // self.pixels

                        # Vérifier si la position dans la matrice est un emplacement valide
                        armes = None
                        if world[row][col] == 1:
                            # Placer l'arme à l'emplacement valide
                            if self.type_arme == "arme_1":
                                armes = Arme(x, y, ARME_1, "arme_1")
                            elif self.type_arme == "arme_2":
                                armes = Arme(x, y, ARME_2, "arme_2")
                            elif self.type_arme == "arme_3":
                                armes = Arme(x, y, ARME_1, "arme_3")
                            else:

                                return
                        if armes is not None:
                            self.towers.append(armes)
                            # Ajoutr la dernière arme ajoutée à mes_armes
                            self.mes_armes.append(self.towers[-1])
                            self.towers[-1].resize_image((50, 50))
                            self.towers[-1].acheter(self)
                            armes.is_placed = True
                            self.arme_placee_recente = True
                            if self.argent > armes.cout_arme < self.prix_arme_definie:
                                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                                self.initial_image_clicked = False

    def maps(self, position_x, position_y, condition_x, condition_y, monde, num):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        Carte.draw_map(self.matrix_height, self.matrix_width, self.pixels, monde, self.screen)

        # Vérifier si tous les monstres ont atteint la position de déclenchement de la prochaine vague
        declancher_prochaine_vague = all(
            monstre.positionX == position_x and monstre.positionY == position_y for monstre in
            self.vagues_de_monstres[self.vague_actuelle])

        if declancher_prochaine_vague:
            self.vague_actuelle += 1
            Carte.afficher_message_vague(self.vague_actuelle, self.window_width, self.window_height, self.screen)

        # Afficher les monstres de la vague actuelle
        vie_joueur = self.vie_joueur.vie_joueur  # Stocker la valeur de vie du joueur pour éviter un accès répété
        mes_armes = self.mes_armes  # Stocker les armes pour éviter un accès répété

        for monstre in self.vagues_de_monstres[self.vague_actuelle]:

            if vie_joueur > 0:
                draw_methods = {
                    1: monstre.draw_monstre_map_1,
                    2: monstre.draw_monstre_map_2,
                    3: monstre.draw_monstre_map_3
                }

            if num in draw_methods:
                draw_method = draw_methods[num]
                draw_method(self.screen, self.pixels)

                monstre.update_velocite_rect()

                positions = (monstre.positionX, monstre.positionY)

            for arme in self.mes_armes:
                Arme.detecter_monstres([arme], positions, 300)

            for projectile in Arme.all_projectiles.copy():
                if projectile.rect.right < 0 or projectile.rect.left > self.window_width or projectile.rect.bottom < 0 or projectile.rect.top > self.window_height:
                    Arme.all_projectiles.remove(projectile)

                else:
                    projectile.draw(self.screen)
                    Monstre.detecter_collision_monstres(self.vagues_de_monstres[self.vague_actuelle], [projectile],
                                                        self)
                    projectile.update()
                # projectile.rec_pro()

            monstre.update_bar_de_vie(self.screen)

            if monstre.positionX == condition_x and monstre.positionY == condition_y:
                self.vie_joueur.degat(monstre.degat, self.screen)

    def displayMove(self, vague, world):
        for monster in vague:
            monster.deplacer(world)
            monster.positions_visitees.append(monster.position_monstre)

            for i in range(len(world)):
                for j in range(len(world[0])):

                    if world[i][j] == 0 or world[i][j] == 5:
                        rect = pygame.Rect(j * self.pixels, i * self.pixels, self.pixels, self.pixels)
                        self.screen.blit(self.image_chemin, rect)
                        
                    elif world[i][j] == 1:
                        rect = pygame.Rect(j * self.pixels, i * self.pixels, self.pixels, self.pixels)
                        self.screen.blit(self.image_mur, rect)

                    elif world[i][j] == 2:
                        rect = pygame.Rect(j * self.pixels, i * self.pixels, self.pixels, self.pixels)
                        self.screen.blit(self.image_menu, rect) 
        
                    self.screen.blit(self.image_monstre, (monster.position_monstre[1] * self.pixels, monster.position_monstre[0] * self.pixels))

            self.horloge.tick(self.vitesse_monstre)
            pygame.display.update()


    def run(self):

        while self.running:
            # On affiche notre Menu et on attend l'action de l'utilisateur pour faire des actions
            # Mais le jeu est demarer avec l'isntance Menu et les changements des etats va permettre d'afficher l'autre screen.
            if self.etat == "menu":
                # on charge notre menu
                self.screen.blit(self.Fond_Menu, (0, 0))
                Button.MenuPrincipal(self.mes_button, self.screen, self)
                #Button.MenuGame(self.mes_button, self.screen, self)

            elif self.etat == "map":
                # self.MenuMap()
                self.world = self.menu_map_screen.MenuMap()

            elif self.etat == "options":
                # On affiche le sous menu d'options
                self.screen.blit(self.Fond_Menu, (0, 0))
                Button.MenuOptions(self.mes_button, self.screen, self, self.sound)

            # Map 1
            elif self.etat == "jeu_map1":
                self.world = world
                self.waves(self.world)
                self.displayMove(self.vagues_de_monstres[self.vague_actuelle], self.world)
                for monstre in self.vagues_de_monstres[self.vague_actuelle]:
                    positions =(monstre.positionX,monstre.positionY)
                    for arme in self.mes_armes:
                        Arme.detecter_monstres([arme], positions, 300)

                    for projectile in Arme.all_projectiles.copy():
                        if projectile.rect.right < 0 or projectile.rect.left > self.window_width or projectile.rect.bottom < 0 or projectile.rect.top > self.window_height:
                            Arme.all_projectiles.remove(projectile)

                        else:
                            projectile.draw(self.screen)
                            Monstre.detecter_collision_monstres(self.vagues_de_monstres[self.vague_actuelle], [projectile],
                                                                self)
                            projectile.update()
                        # projectile.rec_pro()

                    monstre.update_bar_de_vie(self.screen)
                    self.draw()

                    #if monstre.positionX == condition_x and monstre.positionY == condition_y:
                    self.vie_joueur.degat(monstre.degat, self.screen)


            # Map 2
            elif self.etat == "jeu_map2":
                self.world = world_2
                self.waves(self.world)
                self.displayMove(self.vagues_de_monstres[self.vague_actuelle], self.world)

            # Map 3
            elif self.etat == "jeu_map3":
                self.world = world_3
                self.waves(self.world)
                self.displayMove(self.vagues_de_monstres[self.vague_actuelle], self.world)

        pygame.display.flip()

        pygame.quit()
