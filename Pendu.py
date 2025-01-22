solution = "casserole"
tentatives = 7
affichage = ""
for l in solution:
    affichage = affichage + "_ "
lettres_trouvees = ""
lettres_proposees = ""

while tentatives > 0:
    print("Mot à deviner : ", affichage)
    proposition = input("Proposez une lettre : ")
    if proposition in lettres_proposees:
        print("-> Vous avez deja proposé cette lettre!")
        continue
    lettres_proposees += proposition

    if proposition in solution:
        if proposition not in lettres_trouvees:  
            lettres_trouvees = lettres_trouvees + proposition
        print("-> Bien vu!")
    else:
        tentatives = tentatives - 1
        print("-> Nope. Il vous reste", tentatives, "tentatives")


    affichage = ""
    for x in solution:
        if x in lettres_trouvees:
            affichage += x + " "
        else:
            affichage += "_ "

    if "_" not in affichage:
        print(">>> Gagné! <<<")
        break

print("        * Fin de la partie *        ")