import sys
import time

import pygame
from src.componant.AfficheurTexte import AfficheurTexte
from src.Assets.const import *


class Vie:
    def __init__(self):
        self.position_Vie_X = 370
        self.position_Vie_Y = 10
        self.vie_joueur = 100
        self.vie_joueur_max = 100
        self.estVivant = True
        self.restart = pygame.image.load(START)
        self.exit = pygame.image.load(EXIT)

    def afficher_vie_joueur(self, surface):
        couleur_arriere_plan = (60, 63, 60)
        bar_color = (231, 52, 14)
        position = [self.position_Vie_X, self.position_Vie_Y, self.vie_joueur, 10]
        position_arriere_plan = [self.position_Vie_X, self.position_Vie_Y, self.vie_joueur_max, 10]
        pygame.draw.rect(surface, couleur_arriere_plan, position_arriere_plan)
        pygame.draw.rect(surface, bar_color, position)

    def afficher_le_vie(self, screen):
        police = pygame.font.Font(None, 36)

        # créer une surface qui contient le chiffre 100
        texte = police.render(str(self.vie_joueur), True, (255, 255, 255))

        # dessiner le texte sur la surface de jeu
        screen.blit(texte, (370, 10))

    def degat(self, nbr, screen, Map):
        self.vie_joueur -= nbr
        if self.vie_joueur == 0:
            self.estVivant = False
            time.sleep(0.5)
            # Afficher le texte "Game over" sur l'écran
            font = pygame.font.SysFont('Comic Sans MS', 50)
            game_over_text = font.render('Game over', True, (255, 0, 0))
            self.restart = pygame.transform.scale(self.restart, (80, 50))
            self.exit = pygame.transform.scale(self.exit, (80, 50))
            game_over_rect = game_over_text.get_rect()
            game_over_rect.centerx = screen.get_rect().centerx
            game_over_rect.centery = screen.get_rect().centery

            # Afficher le texte "Game over" sur l'écran
            screen.blit(game_over_text, game_over_rect)
            screen.blit(self.restart,(game_over_rect.x+30,game_over_rect.y+50))
            screen.blit(self.exit,(game_over_rect.x+30,game_over_rect.y+120))

            pygame.display.flip()

            # Boucle d'événements pour détecter les événements de fermeture de la fenêtre
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # Si l'utilisateur clique sur la croix de fermeture de la fenêtre
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:  # Si l'utilisateur appuie sur une touche du clavier
                        if event.key == pygame.K_ESCAPE:  # Si l'utilisateur appuie sur la touche "ESCAPE"
                            pygame.quit()
                            sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        restart_button_rect = pygame.Rect(game_over_rect.x+30, game_over_rect.y+50, 80, 50)
                        exit_button_rect = pygame.Rect(game_over_rect.x+30, game_over_rect.y+120, 80,50)
                        if restart_button_rect.collidepoint(mouse_pos):
                            Map.etat="menu"
                            print(Map.etat)
                        elif exit_button_rect.collidepoint(mouse_pos):
                            Map.etat="menu"

