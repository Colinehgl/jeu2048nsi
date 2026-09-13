import random as r

grille = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
nb_cases_vides = 16
score = 0

def init_grille():
    """
    vide la grille
    """
    global score, nb_cases_vides
    score = 0
    for i in range(4):
        for j in range(4):
            grille[i][j] = 0
    nb_cases_vides = 16

def affiche():
    """
    affiche la grille dans la console
    """
    print("")
    for i in range(4):
        for j in range(4):
            print("[", grille[i][j],"]",end="")
        print("")
    print("")

def ajouter():
    """
    ajoute une case dans la grille selon les règles du jeu
    renvoie True si a rajouté, False sinon
    """
    global nb_cases_vides
    if nb_cases_vides == 0:
        return False
    val = 2 * r.randint(1,2)
    pos = r.randint(0, nb_cases_vides - 1)
    i, j = 0, 0
    while True:
        #si on trouve une case vide et que c'est la pos-ième case vide
        if grille[i][j] == 0:
            if pos == 0:
                grille[i][j] = val
                nb_cases_vides -= 1
                return True
            pos -= 1
        # on avance dans tous les cas, case vide ou non
        if j == 3:
            j = 0
            i += 1
        else:
            j += 1
        # i et j ne peuvent pas atteindre 4, sinon nb_cases_vide est faux

def pas_fini():
    """
    vérifie si le jeu n'est pas terminé
    """
    for i in range(4):
        for j in range(4):
            if grille[i][j] == 2048:
                return False
    return True

def deplace_ligne(ligne):
    """
    compresse une ligne vers la gauche
    et fusionne les paires égales adjacentes
    renvoie un triplet (nouvelle ligne, nombre de fusions, score gagné)
    """
    valeurs = [x for x in ligne if x != 0]
    resultat = []
    nb_fusions = 0
    score_gagne = 0
    i = 0
    while i < len(valeurs):
        if i + 1 < len(valeurs) and valeurs[i] == valeurs[i+1]:
            # 2 mêmes valeurs consécutives, on merge
            nouvelle_valeur = valeurs[i] * 2
            resultat.append(nouvelle_valeur)
            score_gagne += nouvelle_valeur  
            # on marque en points la valeur de la case crée par la fusion
            nb_fusions += 1
            i += 2
        else:
            resultat.append(valeurs[i])
            i += 1
    while len(resultat) < 4:
        resultat.append(0)
    return resultat, nb_fusions, score_gagne

def update(moove):
    """
    update le jeu selon l'input du joueur
    4 = gauche, 8 = haut, 2 = bas, 6 = droite
    """
    global nb_cases_vides, score
    match moove:
        case 4:  # gauche
            for i in range(4):
                grille[i], nb_fusions, score_gagne = deplace_ligne(grille[i])
                nb_cases_vides += nb_fusions
                score += score_gagne
            return True

        case 6:  # droite
            for i in range(4):
                ligne_inversee = grille[i][::-1]
                nouvelle, nb_fusions, score_gagne = deplace_ligne(ligne_inversee)
                grille[i] = nouvelle[::-1]
                nb_cases_vides += nb_fusions
                score += score_gagne
            return True

        case 8:  # haut
            for j in range(4):
                colonne = [grille[i][j] for i in range(4)]
                nouvelle, nb_fusions, score_gagne = deplace_ligne(colonne)
                for i in range(4):
                    grille[i][j] = nouvelle[i]
                nb_cases_vides += nb_fusions
                score += score_gagne
            return True

        case 2:  # bas
            for j in range(4):
                colonne = [grille[i][j] for i in range(4)][::-1]
                nouvelle, nb_fusions, score_gagne = deplace_ligne(colonne)
                nouvelle = nouvelle[::-1]
                for i in range(4):
                    grille[i][j] = nouvelle[i]
                nb_cases_vides += nb_fusions
                score += score_gagne
            return True

        case 0:
            return True
        case _:
            return False
    
def lancer():
    """
    fais tourner le jeu
    """
    init_grille()
    affiche()
    while(pas_fini() and ajouter()):
        affiche()
        mv = int(input("moove suivant : "))
        while(not update(mv)):
            print("moove incorrect !")
            mv = int(input("moove suivant : "))
    if pas_fini():
        print("perdu! score final :", score)
    else:
        print("gagné! score final :", score)

#lancer()