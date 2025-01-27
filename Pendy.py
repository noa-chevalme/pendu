import pygame
import random

def charger_mots(fichier):
    with open(fichier, 'r', encoding='utf-8') as f:
        return f.read().splitlines()

pygame.init()

LARGEUR, HAUTEUR = 800, 500
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
game_display = pygame.display.set_mode((800, 500))
bg_image = pygame.image.load('Tableau.jpg')

tous_les_mots = charger_mots('mots.txt')

fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Jeu du Pendu")

police = pygame.font.Font(None, 48)
police_petite = pygame.font.Font(None, 36)

images_pendu = [pygame.image.load(f"Pendu{i}.png") for i in range(7)]
images_pendu = [pygame.transform.scale(pygame.image.load(f"pendu{i}.png"), (350, 350)) for i in range(7)]

def afficher_message(texte, couleur, x, y, centre=False):
    surface = police.render(texte, True, couleur)
    rect = surface.get_rect()
    if centre:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    fenetre.blit(surface, rect)

def jeu_pendu():
    solution = random.choice(tous_les_mots).lower()
    tentatives = 7
    lettres_trouvees = []
    lettres_proposees = []

    en_jeu = True
    while en_jeu:
        game_display.blit(bg_image, (0, 0))
    
        affichage = ""
        for lettre in solution:
            if lettre in lettres_trouvees:
                affichage += lettre + " "
            else:
                affichage += "_ "

        afficher_message("Mot : " + affichage.strip(), BLANC, 50, 50)
        afficher_message(f"Tentatives restantes : {tentatives}", BLANC, 50, 350)
        afficher_message("Lettres proposées : " + ", ".join(lettres_proposees), BLANC, 50, 400)

        if tentatives < 7:
            fenetre.blit(images_pendu[7 - tentatives - 1], (500, 80))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_jeu = False

            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha() and len(event.unicode) == 1:
                    proposition = event.unicode.lower()

                    if proposition in lettres_proposees:
                        afficher_message("Lettre déjà proposée!", ROUGE, 50, 300)
                        pygame.display.flip()
                        pygame.time.wait(1000)
                        continue

                    lettres_proposees.append(proposition)

                    if proposition in solution:
                        lettres_trouvees.append(proposition)
                    else:
                        tentatives -= 1

        if all(lettre in lettres_trouvees for lettre in solution):
            afficher_message(f"Gagné! Le mot était : {solution}", VERT, LARGEUR // 2, HAUTEUR // 2, centre=True)
            pygame.display.flip()
            pygame.time.wait(2000)
            en_jeu = False

        if tentatives <= 0:
            fenetre.blit(images_pendu[-1], (500, 80))
            afficher_message(f"Perdu! Le mot était: {solution}", ROUGE, LARGEUR // 2, HAUTEUR // 2, centre=True)
            pygame.display.flip()
            pygame.time.wait(2000)
            en_jeu = False

jeu_pendu()
pygame.quit()
