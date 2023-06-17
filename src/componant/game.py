import math

import pygame
import time

from src.Assets.const import *

from src.componant.MenuMap import MenuGame
from src.componant.Projectille import Projectile
from src.componant.Sound import Sound
from src.componant.button import *
from src.componant.Monstre import Monstre
from src.componant.Vie import Vie
from src.componant.Armes import Arme
from src.componant.Cartes import Carte
from src.componant.AfficheurTexte import AfficheurTexte
from src.componant.word import *
from src.componant.Wave_monster import Wave_monster

class Map:
    def __init__(self):
        # Pour lancer notre application en boucle
        self.selected_tower = None
        self.running = True
        # titre de notre jeu
        pygame.display.set_caption(TD_TITTLE)
        # on récupère notre matrix que l'on stocke sur un variable
        self.word = word
        # Définir la taille de la matrice et des carrés
        self.matrix_width = len(self.word[0])
        self.matrix_height = len(self.word)

        # la taille de chaque cellule dans le fenetre qu'on met  en pixels
        self.pixels = SIZE
        # Définir la taille de la fenêtre en fonction de notre matrice
        self.window_width = self.matrix_width * self.pixels
        self.window_height = self.matrix_height * self.pixels
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height))
        # charger un image de fond
        self.background = pygame.image.load(BG_SABLE)
        self.background = pygame.transform.scale(self.background, (self.window_width, self.window_height))
        # definir l'image de faire de notre Menu

        self.Fond_Menu = pygame.image.load(FOND_MENU)
        self.Fond_Map = pygame.image.load(FOND_MAP)
        # instanciation de mon menu
        self.mes_button = {
            "title_game": Button(500, 100, TITLE_GAME),
            "button_NewGame": Button(380, 270, NEW_GAME),
            "button_Options": Button(620, 270, OPTION),
            "button_Quit": Button(500, 400, QUIT),
            "button_Icon_Music": Button(400, 200, MUSIQUE_NOTE),
            "button_Icon_Stop_Music": Button(620, 200, DECLINE),
            "button_Retour": Button(520, 360, BACK),
            "coin": Button(780, 475, COIN),
            "kill_game": Button(1010, 480, KILL_GAME)
        }
        self.cartes = {
            "carte_1": Carte(170, 270, CARTE_1),
            "carte_2": Carte(480, 270, CARTE_2),
            "carte_3": Carte(790, 270, CARTE_3),
            "retour": Carte(900, 300, BACK)
        }
        self.text = {
            "text_easy": AfficheurTexte("Facile", 150, 140, (123, 104, 238)),
            "text_medium": AfficheurTexte("Moyen", 430, 140, (123, 104, 238)),
            "text.difficile": AfficheurTexte("Difficile", 750, 140, (123, 104, 238)),
            "game_over": AfficheurTexte("Game Over", 400, 400, (199, 0, 57))
        }
        self.etat_button_options = "normal"
        self.etat = "menu"
        self.en_pause = "play"
        # instancier musiqueS
        self.musiques = LIST_SONG
        self.sound = Sound(self.musiques)
        self.vie_joueur = Vie()
        self.map=0
        # self.armes = {
        #    "arme_1": Arme(715, 40, "Assets/Armes/arme.png", "arme_1")
        # }
        self.mes_armess = [
            Arme(740, 40, WEAPON_RED_LV1, "arme_1"),
            Arme(830, 40, WEAPON_GREEN_LV1, "arme_2"),
            Arme(740, 130, WEAPON_BLUE_LV1, "arme_3")
            # Ajoutez plus d'armes disponibles avec leurs positions
        ]
        self.upgrade = [
            
        ]
        self.mes_armes = []
        self.monstre_positions = []

        # self.vagues_de_monstres = [
        #   [Monstre(84, 480), Monstre(84, 552), Monstre(84, 624)],
        #  [Monstre(84, 480), Monstre(84, 552), Monstre(84, 624)]
        # ]
        self.vagues_de_monstres = []
        ecart_y = 72  # Écart vertical entre chaque vague de monstres
        position_y = 480  # Ordonnée initiale pour la première vague

        for i in range(2):
            vague = [Monstre(84, position_y + (ecart_y * j), 3) for j in
                     range(5)]  # Coordonnées des monstres de la vague i
            self.vagues_de_monstres.append(vague)
            position_y += ecart_y  # Augmenter l'ordonnée initiale pour la prochaine vague

        # Exemple d'utilisation dans un autre fichier
        # vague_monstres = Wave_monster()
        # vague_monstres.generer_vagues(ecart_y=10, nb_vagues=2, nb_monstres_par_vague=5, position_y_initiale=0)

        self.monstres_vague_actuelle = 0
        self.vague_actuelle = 0
        self.position_prochaine_vague = 165
        self.vague_affichee = False
        self.menu_map_screen = MenuGame(self)
        self.click = ""
        self.towers = []
        self.placing_tower = False
        self.selected_weapon = None
        self.argent = 300
        self.arme_placee_recente = True
        self.click_counter = 0
        self.initial_image_clicked = False
        self.arme_initiale = None
        self.type_arme = ""
        self.prix_arme_definie = None
        self.arme_selectionnee = None
        self.joueur_gagnee = False

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
                for arme in self.mes_armes:
                    if arme.rect.collidepoint(x, y):
                        # Vend l'arme
                        self.vendre_arme(arme)
                        self.ameliorer()
                        return

                if not self.initial_image_clicked:
                    for arme in self.mes_armess:

                        if arme.is_clicked_armes((x, y)):
                            arme.cliquer(self)
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
                            self.type_arme = arme.type
                            self.initial_image_clicked = True
                            self.prix_arme_definie = arme.cout_arme
                            self.arme_selectionnee = None

                else:
                    if self.argent >= self.prix_arme_definie:
                        row = y // self.pixels
                        col = x // self.pixels

                        armes = None
                        if world[row][col] == 3:

                            for arme in self.mes_armes:
                                if arme.rect.collidepoint(x, y):

                                    if arme == self.towers[-1]:
                                        self.arme_selectionnee = arme

                                    break

                            if self.type_arme == "arme_1":
                                armes = Arme(x, y, WEAPON_RED_LV1, "arme_1")

                            elif self.type_arme == "arme_2":
                                armes = Arme(x, y, WEAPON_GREEN_LV1, "arme_2")

                            elif self.type_arme == "arme_3":
                                armes = Arme(x, y, WEAPON_BLUE_LV1, "arme_3")
                            else:

                                return

                        if armes is not None:
                            self.towers.append(armes)

                            self.mes_armes.append(self.towers[-1])
                            self.towers[-1].resize_image((40, 40))
                            self.towers[-1].acheter(self)
                            armes.is_placed = True
                            self.arme_placee_recente = True
                            if len(self.mes_armes) > 0:
                                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                                self.initial_image_clicked = False

    def vendre_arme(self, arme):
        self.towers.remove(arme)
        self.mes_armes.remove(arme)
        self.argent += arme.cout_arme
        self.arme_selectionnee = None




    def ameliorer(self):
        image = pygame.image.load(VALIDATION)
        image = pygame.transform.scale(image, (40, 40))
        image_rect = image.get_rect(topleft=(910, 365))
        # if self.etat=="jeu_map1":
        self.screen.blit(image, (910, 365))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # On écoute les evenement du Menu
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # Vérifier si les coordonnées du clic sont à l'intérieur du rectangle de l'image
                if image_rect.collidepoint(mouse):
                    # L'utilisateur a cliqué sur l'image
                    print("Image cliquée !")

    def maps(self, position_x, position_y, condition_x, condition_y, monde, num):
        # for event in pygame.event.get():
        #   if event.type == pygame.QUIT:
        #      self.running = False

        Carte.draw_map(self.matrix_height, self.matrix_width, self.pixels, monde, self.screen)

        # Vérifier si tous les monstres ont atteint la position de déclenchement de la prochaine vague
        declancher_prochaine_vague = all(
            monstre.positionX == position_x and monstre.positionY == position_y for monstre in
            self.vagues_de_monstres[self.vague_actuelle])

        if declancher_prochaine_vague:
            if self.vague_actuelle < len(self.vagues_de_monstres) -1:
                self.vague_actuelle += 1
                Carte.afficher_message_vague(self.vague_actuelle, self.window_width, self.window_height, self.screen)
            else:
                font = pygame.font.SysFont(None, 48)
                message = font.render("Joueur gagné !", True, (255, 255, 255))
                message_rect = message.get_rect(center=(self.window_width // 2, self.window_height // 2))
                self.screen.blit(message, message_rect)
                victory_rect = message.get_rect()
                image = pygame.image.load(CONTINUE)
                image = pygame.transform.scale(image, (80, 60))
                image_quit = pygame.image.load(QUIT)
                image_quit = pygame.transform.scale(image_quit, (80, 60))
                self.screen.blit(image, (victory_rect.x + 450, victory_rect.y + 290))
                self.screen.blit(image_quit, (victory_rect.x + 450, victory_rect.y + 355))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        restart_button_rect = pygame.Rect(victory_rect.x + 450, victory_rect.y + 290, 80, 50)
                        kitt_button_rect = pygame.Rect(victory_rect.x + 450, victory_rect.y + 355, 80, 50)

                        if restart_button_rect.collidepoint(mouse_pos):
                            self.etat = 'menu'
                        elif kitt_button_rect.collidepoint(mouse_pos):
                            self.running=False

        vie_joueur = self.vie_joueur.vie_joueur

        for monstre in self.vagues_de_monstres[self.vague_actuelle]:

            if vie_joueur > 0:
                monstre.draw_monstre(self.screen, self.pixels, self.map)
                monstre.update_velocite_rect()
                positions = (monstre.positionX, monstre.positionY)

            for arme in self.mes_armes:
                Arme.detecter_monstres([arme], positions, 300, self.screen)
                Monstre.afficher_pieces_gagnees(self.screen)

            for projectile in Arme.all_projectiles.copy():
                if projectile.rect.right < 0 or projectile.rect.left > self.window_width or projectile.rect.bottom < 0 or projectile.rect.top > self.window_height:
                    Arme.all_projectiles.remove(projectile)

                else:
                    projectile.draw(self.screen)
                    Monstre.detecter_collision_monstres(self.vagues_de_monstres[self.vague_actuelle], [projectile],self)
                    projectile.update()

            self.mes_button['coin'].afficher_coin(self.screen, self.argent)
            monstre.update_bar_de_vie(self.screen)
            if monstre.positionX == condition_x and monstre.positionY == condition_y:
                self.vie_joueur.degat(monstre.degat, self.screen, self)

    def run(self):

        while self.running:
            # On affiche notre Menu et on attend l'action de l'utilisateur pour faire des actions
            # Mais le jeu est demarer avec l'isntance Menu et les changements des etats va permettre d'afficher l'autre fenetre.
            if self.etat == "menu":
                # on charge notre menu
                self.screen.blit(self.Fond_Menu, (0, 0))
                Button.MenuPrincipal(self.mes_button, self.screen, self)
                # Button.MenuGame(self.mes_button, self.screen, self)

            elif self.etat == "map":
                # self.MenuMap()
                self.menu_map_screen.MenuMap()

            elif self.etat == "options":
                # On affiche le sous menu d'options
                self.screen.blit(self.Fond_Menu, (0, 0))
                Button.MenuOptions(self.mes_button, self.screen, self, self.sound)

            # Map 1
            elif self.etat == "jeu_map1":

                self.maps(165, -78, 165, -69, word, 1)
                self.verifier_le_click_sur_quel_image(word)
                self.draw()
                self.vie_joueur.afficher_vie_joueur(self.screen)

                pygame.display.update()

            # Map 2
            elif self.etat == "jeu_map2":
                self.maps(444, -78, 444, -69, word_2, 2)
                self.verifier_le_click_sur_quel_image(word_2)
                # Button.MenuGame(self.mes_button, self.screen, self)
                self.draw()
                self.vie_joueur.afficher_vie_joueur(self.screen)
                pygame.display.update()

            # Map 3
            elif self.etat == "jeu_map3":
                self.maps(165, -78, 165, -69, word_3, 3)
                self.verifier_le_click_sur_quel_image(word_3)
                # Button.MenuGame(self.mes_button, self.screen, self)
                self.draw()
                self.vie_joueur.afficher_vie_joueur(self.screen)
                pygame.display.update()

        pygame.display.flip()

        pygame.quit()
