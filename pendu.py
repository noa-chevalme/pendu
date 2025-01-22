import random

with open('mots.txt', 'r', encoding='utf-8') as fichier:
    mots = fichier.read().splitlines()

while True:  
    solution = random.choice(mots).lower()  
    tentatives = 7
    affichage = "_ " * len(solution)
    lettres_trouvees = ""
    lettres_proposees = ""

    while tentatives > 0:
        print("\nMot à deviner :", affichage.strip())  
        proposition = input("Proposez une lettre ou devinez le mot : ").lower()  

        if len(proposition) > 1: 
            if proposition == solution:
                print("\n>>> Gagné! Le mot était :", solution)
                break
            else:
                tentatives -= 1
                print(f"-> Mauvaise tentative! Il vous reste {tentatives} tentatives.")
                continue

        if not proposition.isalpha() or len(proposition) != 1:
            print("-> Entrez une seule lettre valide ou essayez de deviner le mot.")
            continue

        if proposition in lettres_proposees:
            print("-> Vous avez déjà proposé cette lettre!")
            continue
        lettres_proposees += proposition

        if proposition in solution:
            if proposition not in lettres_trouvees:
                lettres_trouvees += proposition 
            print("-> Bien vu!")
        else:
            tentatives -= 1
            print(f"-> Nope. Il vous reste {tentatives} tentatives.")

        affichage = ""
        for x in solution:
            if x in lettres_trouvees:
                affichage += x + " "
            else:
                affichage += "_ "

        if "_" not in affichage:
            print("\n>>> Gagné! Le mot était :", solution)
            break

    if tentatives == 0:
        print(f"\n>>> Perdu! Le mot était : {solution}")

    choix = input("\nVoulez-vous rejouer ? (o/n) : ").lower()
    if choix != 'o':
        print("\nMerci d'avoir joué! À bientôt!")
        break
