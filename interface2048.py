import tkinter as tk
import jeu2048 as jeu  # notre module avec toute la logique du jeu

def copie_grille():
    """
    renvoie une copie de la grille (pour comparer avant/après un mouvement)
    """
    return [ligne[:] for ligne in jeu.grille]

def couleur(valeur):
    """
    renvoie une couleur de fond différente selon la valeur de la case
    (juste pour faire un peu plus joli, pas obligatoire)
    """
    couleurs = {
        2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
        32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
        512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
    }
    return couleurs.get(valeur, "#3c3a32")

def actualise_affichage():
    """
    met à jour les labels de la grille et le score affiché
    """
    for i in range(4):
        for j in range(4):
            valeur = jeu.grille[i][j]
            if valeur == 0:
                labels[i][j].config(text="", bg="#cdc1b4")
            else:
                labels[i][j].config(text=str(valeur), bg=couleur(valeur))
    label_score.config(text="Score : " + str(jeu.score))

def jouer(moove):
    """
    fait un mouvement, ajoute une nouvelle case seulement si la grille
    a changé, puis vérifie si la partie est terminée
    """
    avant = copie_grille()
    jeu.update(moove)
    if jeu.grille != avant:
        jeu.ajouter()
    actualise_affichage()
    if not jeu.pas_fini():
        label_score.config(text="Gagné ! Score final : " + str(jeu.score))
    elif jeu.nb_cases_vides == 0 and jeu.grille == avant:
        # plus de case vide et le dernier mouvement n'a rien changé : on est bloqué
        # (test simple, ne vérifie pas si un AUTRE mouvement resterait possible)
        label_score.config(text="Perdu ! Score final : " + str(jeu.score))

def touche_pressee(event):
    """
    associe chaque flèche du clavier à un mouvement du jeu
    """
    if event.keysym == "Left":
        jouer(4)
    elif event.keysym == "Up":
        jouer(8)
    elif event.keysym == "Down":
        jouer(2)
    elif event.keysym == "Right":
        jouer(6)

# création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("2048")

# le score affiché en haut
label_score = tk.Label(fenetre, text="Score : 0", font=("Arial", 16))
label_score.grid(row=0, column=0, columnspan=4, pady=10)

# la grille de jeu : un tableau de Label, un par case
labels = []
for i in range(4):
    ligne_labels = []
    for j in range(4):
        lbl = tk.Label(fenetre, text="", width=4, height=2,
                        font=("Arial", 24, "bold"), bg="#cdc1b4")
        lbl.grid(row=i + 1, column=j, padx=5, pady=5)
        ligne_labels.append(lbl)
    labels.append(ligne_labels)

# 4 boutons, au cas où les flèches du clavier ne marchent pas bien
bouton_haut = tk.Button(fenetre, text="▲", width=4, command=lambda: jouer(8))
bouton_haut.grid(row=5, column=1, columnspan=2)

bouton_gauche = tk.Button(fenetre, text="◄", width=4, command=lambda: jouer(4))
bouton_gauche.grid(row=6, column=0)

bouton_bas = tk.Button(fenetre, text="▼", width=4, command=lambda: jouer(2))
bouton_bas.grid(row=6, column=1, columnspan=2)

bouton_droite = tk.Button(fenetre, text="►", width=4, command=lambda: jouer(6))
bouton_droite.grid(row=6, column=3)

# on associe les touches du clavier à la fonction touche_pressee
# (il faut que la fenêtre ait le focus pour que ça marche)
fenetre.bind("<Key>", touche_pressee)

# initialisation de la partie : grille vide + 2 cases de départ
jeu.init_grille()
jeu.ajouter()
jeu.ajouter()
actualise_affichage()

fenetre.mainloop()