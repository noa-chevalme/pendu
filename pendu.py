import pygame
import random
import os
import unicodedata

# Fonction pour enlever les accents des caractères
def enlever_accents(texte):
    return ''.join(c for c in unicodedata.normalize('NFD', texte) if unicodedata.category(c) != 'Mn')

def charger_mots(fichier):
    with open(fichier, 'r', encoding='utf-8') as f:
        return f.read().splitlines()

def enregistrer_score(pseudo, score):
    with open("score.txt", "a", encoding="utf-8") as fichier:
        fichier.write(f"{pseudo} : {score}\n")

def afficher_leaderboard():
    if not os.path.exists("score.txt"):
        return []
    with open("score.txt", "r", encoding="utf-8") as fichier:
        scores = fichier.readlines()

    # Trier les scores par ordre décroissant
    scores = sorted(scores, key=lambda x: int(x.split(" : ")[1]), reverse=True)

    return [score.strip() for score in scores]

pygame.init()

# Initialisation du module de son
pygame.mixer.init()

# Chargement des sons
son_bonne_lettre = pygame.mixer.Sound("bonne_lettre.mp3")
son_mauvaise_lettre = pygame.mixer.Sound("mauvaise_lettre.mp3")
son_defaite = pygame.mixer.Sound("defaite.mp3")
son_initialisation = pygame.mixer.Sound("initialisation_jeu.mp3")
son_leaderboard = pygame.mixer.Sound("leaderboard.mp3")

# Dimensions et couleurs
LARGEUR, HAUTEUR = 800, 500
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)

# Fenêtre de jeu
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Jeu du Pendu")

# Polices
police = pygame.font.Font(None, 48)
police_petite = pygame.font.Font(None, 36)

# Images
bg_image = pygame.image.load('Tableau.jpg')
images_pendu = [pygame.transform.scale(pygame.image.load(f"pendu{i}.png"), (350, 350)) for i in range(7)]

# Fonction d'affichage de texte
def afficher_message(texte, couleur, x, y, centre=False):
    surface = police.render(texte, True, couleur)
    rect = surface.get_rect()
    if centre:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    fenetre.blit(surface, rect)

# Menu pour choisir la difficulté
def choisir_difficulte():
    en_jeu = True
    choix = None
    while en_jeu:
        fenetre.fill(NOIR)
        afficher_message("Choisissez la difficulté :", BLANC, LARGEUR // 2, HAUTEUR // 4, centre=True)
        afficher_message("[1] Facile", BLANC, LARGEUR // 2, HAUTEUR // 2 - 40, centre=True)
        afficher_message("[2] Moyen", BLANC, LARGEUR // 2, HAUTEUR // 2, centre=True)
        afficher_message("[3] Difficile", BLANC, LARGEUR // 2, HAUTEUR // 2 + 40, centre=True)
        afficher_message("[L] Leaderboard", BLANC, LARGEUR // 2, HAUTEUR // 2 + 80, centre=True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    choix = ("facile.txt", 50)
                    en_jeu = False
                elif event.key == pygame.K_2:
                    choix = ("moyen.txt", 100)
                    en_jeu = False
                elif event.key == pygame.K_3:
                    choix = ("difficile.txt", 200)
                    en_jeu = False
                elif event.key == pygame.K_l:
                    leaderboard = afficher_leaderboard()
                    afficher_leaderboard_écran(leaderboard)
    return choix

# Affichage du leaderboard
def afficher_leaderboard_écran(leaderboard):
    en_jeu = True
    son_leaderboard.play()  # Jouer le son du leaderboard
    while en_jeu:
        fenetre.fill(NOIR)
        afficher_message("Leaderboard :", BLANC, LARGEUR // 2, 50, centre=True)
        y = 100
        for score in leaderboard[:10]:  # Afficher les 10 premiers scores
            afficher_message(score, BLANC, LARGEUR // 2, y, centre=True)
            y += 30
        afficher_message("[Retour : Echap]", ROUGE, LARGEUR // 2, HAUTEUR - 50, centre=True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    en_jeu = False

# Écran Game Over
def game_over(score, afficher_leaderboard_après=False, afficher_écran_de_defaite=True):
    if afficher_écran_de_defaite:
        son_defaite.play()  # Jouer le son de défaite
        en_jeu = True
        pseudo = ""
        while en_jeu:
            fenetre.fill(NOIR)
            afficher_message("Game Over!", ROUGE, LARGEUR // 2, HAUTEUR // 4, centre=True)
            afficher_message(f"Votre score : {score}", BLANC, LARGEUR // 2, HAUTEUR // 2 - 50, centre=True)
            afficher_message("Entrez votre pseudo :", BLANC, LARGEUR // 2, HAUTEUR // 2, centre=True)
            afficher_message(pseudo, BLANC, LARGEUR // 2, HAUTEUR // 2 + 50, centre=True)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and pseudo:
                        enregistrer_score(pseudo, score)
                        en_jeu = False
                    elif event.key == pygame.K_BACKSPACE:
                        pseudo = pseudo[:-1]
                    elif event.unicode.isalnum():
                        pseudo += event.unicode

    if afficher_leaderboard_après:
        leaderboard = afficher_leaderboard()
        afficher_leaderboard_écran(leaderboard)

# Fonction pour demander si on rejoue
def demander_rejouer(score):
    en_jeu = True
    choix = None
    while en_jeu:
        fenetre.fill(NOIR)
        afficher_message("Voulez-vous rejouer ?", BLANC, LARGEUR // 2, HAUTEUR // 3, centre=True)
        afficher_message("[O] Oui", BLANC, LARGEUR // 2, HAUTEUR // 2 - 20, centre=True)
        afficher_message("[N] Non", BLANC, LARGEUR // 2, HAUTEUR // 2 + 20, centre=True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    choix = True
                    en_jeu = False
                elif event.key == pygame.K_n:
                    choix = False
                    en_jeu = False
    return choix

# Jeu du pendu
def jeu_pendu():
    total_score = 0  # Score global qui s'accumule entre les parties
    jouer = True
    son_initialisation.play()  # Jouer le son d'initialisation du jeu
    while jouer:
        # Choisir la difficulté
        fichier_difficulte, score_bonus = choisir_difficulte()
        tous_les_mots = charger_mots(fichier_difficulte)
        solution = enlever_accents(random.choice(tous_les_mots).lower())

        # Variables de jeu
        tentatives = 7
        lettres_trouvees = []
        lettres_proposees = []
        score_partie = 0  # Score de la partie actuelle
        en_jeu = True

        while en_jeu:
            fenetre.blit(bg_image, (0, 0))

            # Afficher le mot à deviner
            affichage = ""
            for lettre in solution:
                if lettre in lettres_trouvees:
                    affichage += lettre + " "
                else:
                    affichage += "_ "
            afficher_message("Mot : " + affichage.strip(), BLANC, 50, 50)
            afficher_message(f"Tentatives restantes : {tentatives}", BLANC, 50, 350)
            afficher_message("Lettres proposées : " + ", ".join(lettres_proposees), BLANC, 50, 400)

            # Afficher le score
            afficher_message(f"Score : {total_score + score_partie}", BLANC, 50, 450)

            # Afficher l'image du pendu
            if tentatives < 7:
                fenetre.blit(images_pendu[7 - tentatives - 1], (500, 80))
            pygame.display.flip()

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        continue  # Ignore Backspace, pas besoin de gérer l'entrée
                    elif event.key == pygame.K_RETURN:
                        continue  # Ignore le retour à la ligne
                    if event.unicode.isalpha():
                        proposition = enlever_accents(event.unicode.lower())  # Normaliser la proposition
                        if proposition in lettres_proposees:
                            continue
                        lettres_proposees.append(proposition)
                        if proposition in solution:
                            lettres_trouvees.append(proposition)
                            score_partie += 10
                            son_bonne_lettre.play()  # Jouer le son de bonne lettre
                        else:
                            tentatives -= 1
                            son_mauvaise_lettre.play()  # Jouer le son de mauvaise lettre

            # Conditions de victoire ou défaite
            if all(lettre in lettres_trouvees for lettre in solution):
                score_partie += score_bonus  # Ajouter le bonus à la fin du mot
                en_jeu = False
            if tentatives <= 0:
                game_over(total_score + score_partie, afficher_leaderboard_après=True, afficher_écran_de_defaite=True)
                en_jeu = False

        # Ajouter le score de cette partie au score global
        total_score += score_partie

        # Demander si on rejoue
        jouer = demander_rejouer(total_score)

# Lancer le jeu
jeu_pendu()
pygame.quit()
