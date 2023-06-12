import math
import pygame
import time
from MenuMap import MenuGame
from Projectille import Projectile
from Sound import Sound
from button import Button
from Monstre import Monstre
from Vie import Vie
from Armes import Arme
from Cartes import Carte
from AfficheurTexte import AfficheurTexte
from word import *

class Map:
    def __init__(self):
        # Pour lancer notre application en boucle
        self.selected_tower = None
        self.running = True
        # titre de notre jeu
        pygame.display.set_caption("Tower Defense")
        # on récupère notre matrix que l'on stocke sur un variable
        self.word = word
        # Définir la taille de la matrice et des carrés
        self.matrix_width = len(self.word[0])
        self.matrix_height = len(self.word)
        self.fenetre = pygame.display.set_mode((self.matrix_width, self.matrix_height))
        # la taille de chaque cellule dans le fenetre qu'on met  en pixels
        self.pixels = 40
        # Définir la taille de la fenêtre en fonction de notre matrice
        self.window_width = self.matrix_width * self.pixels
        self.window_height = self.matrix_height * self.pixels
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        # charger un image de fond
        self.background = pygame.image.load("Assets/sable.jpg")
        self.background = pygame.transform.scale(self.background, (self.window_width, self.window_height))
        self.Fond_Menu = pygame.image.load("Assets/BackTest.png")
        self.Fond_Map = pygame.image.load("Assets/Cartes/map_1.png")
        self.Fond_Map = pygame.image.load("Assets/Cartes/map_1.png")
        # instanciation de mon menu
        self.mes_button = {
            "button_Menu": Button(500, 100,"Assets/logo2-removebg-preview.png"),
            "button_NewGame": Button(380, 270,"Assets/Buttons/New_Game.png"),
            "button_Options": Button(620, 270,"Assets/Buttons/Options.png"),
            "button_Quitt": Button(500, 400,"Assets/Buttons/Quit.png"),
            "button_SousMenuMusique": Button(400, 100,"Assets/Buttons/Music_note_icon.png"),
            "button_SousMenuStopMusique": Button(620, 100,"Assets/Buttons/Decline.png"),
            "button_SousMenuAudio": Button(400, 250,"Assets/Buttons/Music_note_icon.png"),
            "button_SousMenuStopAudio": Button(620, 250,"Assets/Buttons/Decline.png"),
            "button_Retour": Button(520, 420,"Assets/Buttons/Back.png")
        }
        self.cartes = {
            "carte_1": Carte(170, 270, "Assets/Cartes/map_1.png"),
            "carte_2": Carte(480, 270, "Assets/Cartes/map_2.png"),
            "carte_3": Carte(790, 270, "Assets/Cartes/map_3.png"),
            "retour": Carte(900, 300, "Assets/Armes/button.jpg")
        }
        self.text = {
            "text_easy": AfficheurTexte("Facile", 150, 140, (123,104,238)),
            "text_medium": AfficheurTexte("Moyen", 430, 140, (123,104,238)),
            "text.difficile": AfficheurTexte("Difficile", 750, 140, (123,104,238)),
            "game_over": AfficheurTexte("Game Over", 400, 400, (199, 0, 57))
        }
        self.etat_button_options = "normal"
        self.etat = "menu"
        self.sound = Sound("Musique/1.mp3")
        self.vie_joueur = Vie()
        # self.armes = {
        #    "arme_1": Arme(715, 40, "Assets/Armes/arme.png", "arme_1")
        # }
        self.mes_armess = [
            Arme(715, 40, "Assets/Armes/armes-removebg-preview.png", "arme_1"),
            Arme(820, 40, "Assets/Armes/Basic2 howitzer moving_waifu2x_photo_noise3_scale.png", "arme_2")
            # Ajoutez plus d'armes disponibles avec leurs positions
        ]
        self.mes_armes = []
        self.monstre_positions = []

        self.vagues_de_monstres = [
            [Monstre(84, 480)],
            [Monstre(84, 480), Monstre(84, 552), Monstre(84, 624)]
        ]
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

        #-------------------------------------
        self.vitesse_monstre = 5
        self.horloge = pygame.time.Clock()

        self.image_monstre = pygame.image.load('Assets/Monsters/Turtle_monster.png')
        self.image_monstre = pygame.transform.scale(self.image_monstre, (self.pixels, self.pixels))

        self.image_mur = pygame.image.load('Assets/Armes/wals.png')
        self.image_mur = pygame.transform.scale(self.image_mur, (self.pixels, self.pixels))

        self.image_chemin = pygame.image.load('Assets/sable.jpg')
        self.image_chemin = pygame.transform.scale(self.image_chemin, (self.pixels, self.pixels))

        self.image_menu = pygame.image.load("Assets/Armes/Image 89 at frame 1copy .jpg")
        self.image_menu = pygame.transform.scale(self.image_menu, (self.pixels, self.pixels))

        self.pos_monstre = [11, 1]
        self.positions_visitees = []
        
        self.terrain = [

        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 2, 2, 2, 2, 2, 2, 2],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2, 2, 2, 2, 2, 2, 2],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2, 2, 2, 2, 2, 2, 2],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 2, 2, 2, 2, 2, 2, 2],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 2, 2, 2, 2, 2, 2, 2],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 2, 2, 2, 2, 2, 2, 2],
        [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 2, 2, 2, 2, 2, 2, 2],
        [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 2, 2, 2, 2, 2, 2, 2],
        [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 2, 2, 2, 2, 2, 2, 2],
        [1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2],

        ]

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
                                armes = Arme(x, y, "Assets/Armes/armes-removebg-preview.png", "arme_1")
                            elif self.type_arme == "arme_2":
                                armes = Arme(x, y, "Assets/Armes/Basic2 howitzer moving_waifu2x_photo_noise3_scale.png","arme_2")
                            elif self.type_arme == "arme_3":
                                armes = Arme(x, y, "Assets/Armes/arme_3.png", "arme_3")
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

                positions = (monstre.positionX, monstre.positionY)

            for arme in self.mes_armes:
                Arme.detecter_monstres([arme], positions, 300)

            for projectile in Arme.all_projectiles.copy():
                if projectile.rect.right < 0 or projectile.rect.left > self.window_width or projectile.rect.bottom < 0 or projectile.rect.top > self.window_height:
                    Arme.all_projectiles.remove(projectile)

                else:
                    monstre.detecter_collision_projectile([projectile])
                    projectile.update()
                    projectile.draw(self.screen)

            monstre.update_bar_de_vie(self.screen)

            if monstre.positionX == condition_x and monstre.positionY == condition_y:
                self.vie_joueur.degat(monstre.degat, self.screen)

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

        while self.running:
            # On affiche notre Menu et on attend l'action de l'utilisateur pour faire des actions
            # Mais le jeu est demarer avec l'isntance Menu et les changements des etats va permettre d'afficher l'autre fenetre.
            if self.etat == "menu":
                # on charge notre menu
                self.screen.blit(self.Fond_Menu, (0, 0))
                Button.MenuPrincipal(self.mes_button, self.screen, self)

            elif self.etat == "map":
                # self.MenuMap()
                self.menu_map_screen.MenuMap()

            elif self.etat == "options":
                # On affiche le sous menu d'options
                self.screen.blit(self.Fond_Menu, (0, 0))
                Button.MenuOptions(self.mes_button, self.screen, self, self.sound)

            # Map 1
            elif self.etat == "jeu_map1":
                # self.maps(165, -78, 165, -69, word, 1)
                # self.verifier_le_click_sur_quel_image(word)
                # self.draw()
                # self.vie_joueur.afficher_vie_joueur(self.screen)
                # pygame.display.update()

                #--------------------------------------------------

                self.deplacer()
                self.positions_visitees.append(self.pos_monstre)

                for i in range(len(self.terrain)):
                    for j in range(len(self.terrain[0])):

                        if self.terrain[i][j] == 0:
                            rect = pygame.Rect(j * self.pixels, i * self.pixels, self.pixels, self.pixels)
                            self.fenetre.blit(self.image_chemin, rect)
                            
                        elif self.terrain[i][j] == 1:
                            rect = pygame.Rect(j * self.pixels, i * self.pixels, self.pixels, self.pixels)
                            self.fenetre.blit(self.image_mur, rect)

                        elif self.terrain[i][j] == 2:
                            rect = pygame.Rect(j * self.pixels, i * self.pixels, self.pixels, self.pixels)
                            self.fenetre.blit(self.image_menu, rect) 

                self.fenetre.blit(self.image_monstre, (self.pos_monstre[1] * self.pixels, self.pos_monstre[0] * self.pixels))

                pygame.display.update()
                self.horloge.tick(self.vitesse_monstre)

            # Map 2
            elif self.etat == "jeu_map2":
                self.maps(444, -78, 444, -69, word_2, 2)
                self.verifier_le_click_sur_quel_image(word_2)
                self.draw()
                self.vie_joueur.afficher_vie_joueur(self.screen)
                pygame.display.update()

            # Map 3
            elif self.etat == "jeu_map3":
                self.maps(165, -78, 165, -69, word_3, 3)
                self.verifier_le_click_sur_quel_image(word_3)
                self.draw()
                self.vie_joueur.afficher_vie_joueur(self.screen)
                print(self.argent)
                pygame.display.update()

        pygame.display.flip()

        pygame.quit()