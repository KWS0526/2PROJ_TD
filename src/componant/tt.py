import pygame

# Initialisation de Pygame
pygame.init()

# Définition des dimensions de la fenêtre principale
largeur = 800
hauteur = 600

# Création de la fenêtre principale
fenetre_principale = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Fenêtre de jeu")

# Couleurs (vous pouvez personnaliser les couleurs selon vos préférences)
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

# Définition des dimensions de la fenêtre secondaire
fenetre_secondaire_largeur = 400
fenetre_secondaire_hauteur = 300

# Coordonnées de la fenêtre secondaire
fenetre_secondaire_x = (largeur - fenetre_secondaire_largeur) // 2
fenetre_secondaire_y = (hauteur - fenetre_secondaire_hauteur) // 2

# Création de la fenêtre secondaire
fenetre_secondaire = pygame.Surface((fenetre_secondaire_largeur, fenetre_secondaire_hauteur))
fenetre_secondaire.fill(BLANC)

# Boucle principale du jeu
en_cours = True
while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            if evenement.button == 1:  # Clic gauche de la souris
                # Vérification si le clic est à l'intérieur de la fenêtre principale
                if fenetre_secondaire_x <= evenement.pos[0] <= fenetre_secondaire_x + fenetre_secondaire_largeur and \
                   fenetre_secondaire_y <= evenement.pos[1] <= fenetre_secondaire_y + fenetre_secondaire_hauteur:
                    print("Clic dans la fenêtre secondaire")

    # Affichage
    fenetre_principale.fill(NOIR)
    fenetre_principale.blit(fenetre_secondaire, (fenetre_secondaire_x, fenetre_secondaire_y))
    pygame.display.flip()

# Fermeture de Pygame
pygame.quit()

