import pygame

from src.Assets.const import *

class Button:
    # le constrcteur pour creer un bouton Menu
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (200, 100)).convert()
        self.rect = self.image.get_rect(center=(x, y))
        self.start = False
        self.menu_optons = pygame.image.load(image_path)

    # cet fonction permet de verifier si notre button est cliquer
    def is_clicked(self, position):
        # verifie si le bouton et le souris sont au meme coordonnes au clik
        if self.rect.collidepoint(position):
            self.start = True
            return True
        else:
            return False

    def Options(self):
        return self.image_options

    @classmethod
    #lance la musique
    def option_play_Musique(cls, mes_button, screen, sound):
        # On remplace le bouton par un nouveau
        new_button = cls(620, 200, ICON_PLAY)
        mes_button["button_Icon_Music"] = new_button
        screen.blit(mes_button["button_Icon_Music"].image, mes_button["button_Icon_Music"].rect)
        sound.play_sound()

    # stop la musique
    @classmethod
    def option_stop_Musique(cls, mes_button, screen, sound):
        # On remet le boutton initial
        new_button = cls(620, 200, ICON_PAUSE)
        mes_button["button_Icon_Stop_Music"] = new_button
        screen.blit(mes_button["button_Icon_Stop_Music"].image, mes_button["button_Icon_Stop_Music"].rect)
        sound.stop_sound()

    @classmethod
    def kill_jeu(cls, mes_button, screen, Map):
        new_button= cls(1010,480, KILL_GAME)
        mes_button["kill_game"]=new_button
        mes_button["kill_game"].image = pygame.transform.scale(mes_button["kill_game"].image, (40, 30))
        screen.blit(mes_button["kill_game"].image, mes_button["kill_game"].rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Map.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mes_button["kill_game"].is_clicked(pygame.mouse.get_pos()):
                    Map.etat = "menu"

    @classmethod
    def MenuPrincipal(cls, mes_button, screen, Map):
        # self.screen.blit(self.Fond_Menu, (0, 0))
        # on charge le Menu
        screen.blit(mes_button["title_game"].image, mes_button["title_game"].rect)
        screen.blit(mes_button["button_NewGame"].image, mes_button["button_NewGame"].rect)
        screen.blit(mes_button["button_Options"].image, mes_button["button_Options"].rect)
        screen.blit(mes_button["button_Quit"].image, mes_button["button_Quit"].rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Map.running = False
            # On écoute les evenement du Menu
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mes_button["button_NewGame"].is_clicked(pygame.mouse.get_pos()):
                    # si c'est le bouton New Game est (clique) on change l'etat du jeu pour quitter fenetre menu pour aller fenetre dujeux

                    Map.etat = "map"
                elif mes_button["button_Options"].is_clicked(pygame.mouse.get_pos()):
                    # si c'est le bouton options est (clique) on change l'etat du jeu pour quitter fenetre menu pour aller fenetre des options
                    Map.etat = "options"
                elif mes_button["button_Quit"].is_clicked(pygame.mouse.get_pos()):
                    Map.running = False
        pygame.display.flip()

    def afficher_coin(self, screen, argent):
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.image.set_colorkey((0, 0, 0))
        screen.blit(self.image, self.rect)
        police = pygame.font.Font(None, 30)
        texte_montant = police.render("{}".format(argent), True, (255, 255, 255))
        screen.blit(texte_montant, (self.rect.right - 130, self.rect.top + 40))
    
    @classmethod
    def ameliorer(cls,Map):
        image = pygame.image.load(VALIDATION)
        image = pygame.transform.scale(image, (40, 40))
        image_rect = image.get_rect(topleft=(910, 365))
        if Map.etat=="jeu_map1":
            Map.screen.blit(image,(910,365))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Map.running = False
                # On écoute les evenement du Menu
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    # Vérifier si les coordonnées du clic sont à l'intérieur du rectangle de l'image
                    if image_rect.collidepoint(mouse):
                        # L'utilisateur a cliqué sur l'image
                        print("Image cliquée !")

    @classmethod
    def MenuOptions(cls, mes_button, screen, Map, sound):
        # On affiche les Boutons du Sous Menues Options
        screen.blit(mes_button["button_Icon_Music"].image, mes_button["button_Icon_Music"].rect)
        screen.blit(mes_button["button_Icon_Stop_Music"].image,mes_button["button_Icon_Stop_Music"].rect)
        screen.blit(mes_button["button_Retour"].image, mes_button["button_Retour"].rect)

        # On écoute les événements sur les Boutons et attribue des états
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Map.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # BUTTON RETOUR
                if mes_button["button_Retour"].is_clicked(pygame.mouse.get_pos()):
                    Map.etat = "menu"

                # BUTTON STOP MUSIC
                elif mes_button["button_Icon_Stop_Music"].is_clicked(pygame.mouse.get_pos()):
                    Map.etat_button_options = "musique"
                    if Map.etat_button_options == "musique":
                        Button.option_stop_Musique(mes_button, screen, sound)

                # BUTTON PLAY MUSIC
                elif mes_button["button_Icon_Music"].is_clicked(pygame.mouse.get_pos()):
                    if Map.etat_button_options == "musique":
                        Map.etat_button_options = "stop_musique"
                    if Map.etat_button_options == "stop_musique":
                        Button.option_play_Musique(mes_button, screen, sound)

        pygame.display.flip()
