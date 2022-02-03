"""
    @ Amina Khalane
    @ Djelni Abdel Malik
    @ RANDRIAMAROMANANA Manarivo

                                PROJET BATAILLE NAVALE TD3 INFORMATIQUE
"""
from random import randrange
from re import search
#BONUS CHANGEMENT DE COULEURS DE L'AFFICHAGE
class color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BLUE = "\033[0;34m"
    LIGHT_PURPLE = "\033[1;35m"

# Constantes
N = 10
COLONNES = [str(i) for i in range(N)]
LIGNES = [' '] + list(map(chr, range(97, 107)))
DICT_LIGNES_INT = {LIGNES[i]: i - 1 for i in range(len(LIGNES))}
VIDE = color.BLUE + '.' + color.RESET #COULEUR BLEU
EAU = color.RED + 'o' + color.RESET #COULEUR ROUGE
TOUCHE = color.GREEN + 'x' + color.RESET #COULEUR VERTE
BATEAU = color.LIGHT_PURPLE + '#' + color.RESET
DETRUIT = color.YELLOW + '@' + color.RESET #COULEUR JAUNE
NOMS = ['Transporteur', 'Cuirassé', 'Croiseur', 'Sous-marin', 'Destructeur']
TAILLES = [5, 4, 3, 3, 2]

def create_grid():
    """Fonction qui crée une matrice de taille N * N"""
    L = [[VIDE for x in range(N)] for x in range(N)]
    return L

def plot_grid(m):
    """Fonction qui affiche la grille de jeu avec les lignes/colonnes """
    m.insert(0, COLONNES)
    for i in range(len(m)):
        m[i].insert(0, LIGNES[i])
    for x in m:
        print(" ".join(x))
    return ""

def tir(m, pos, flotte):
    """Fonction qui tire sur les positions passées en parametre"""
    p=pos_from_string(pos)
    if m[p[0]][p[1]] != VIDE :
        print("Position déjà attaquée !")
        return False
    else:
        if presence_bateau(p, flotte) == True:
            print("Touché !")
            m[p[0]][p[1]] = TOUCHE
            f=flotte[id_bateau_at_pos(p,flotte)]
            f["cases touchés"] += 1
            if f["cases touchés"] == f["taille"]:
                print("Touché ! Coulé ! pour "+f["nom"])
                flotte.pop(id_bateau_at_pos(p,flotte))
                for x in f["positions"]:
                    m[x[0]][x[1]]=DETRUIT
            return True
        else:
            m[p[0]][p[1]] = EAU
            print("Manquée !")
            return False

def random_position():
    """Fonctio qui renvoie aléatoirement une paire d'entier entre 0 et N """
    x = randrange(0, N)
    y = randrange(0, N)
    return x, y

def pos_from_string(S):
    """Fonction qui transforme une chaine de caractère en coordonnée pour la grille de jeu"""
    xlignes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    ycolonnes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    l = S.split()
    if l[0] in xlignes:
        a = xlignes.index(l[0])
    while l[0] not in xlignes:
        print("Coordonnées non valides (lettre comprise entre a et j puis chiffre compris entre 0-9)")
        l[0] = input("entrer une lettre comprise entre a et j : ")
    a = xlignes.index(l[0])

    if int(l[1]) in ycolonnes:
        b = int(l[1])
    while l[1] not in ycolonnes:
        print("Coordonnées non valides (lettre comprise entre a et j puis chiffre compris entre 0-9)")
        l[1] = input("entrer un chiffre compris entre 0 et 9 : ")
    b = int(l[1])
    return (a, b)

def nouveau_bateau(flotte, nom, taille, pos, orientation):
    """Fonction qui rajoute les informations sur un bateau dans une liste de dictionnaire"""
    # 'orientation':orientation
    xlignes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    ycolonnes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    pos_s = 0
    if (orientation == 'v'):
        pos_s = [(pos[0] + i, pos[1]) for i in range(taille)]
        for i in range(taille):
            if (pos[0] + i not in ycolonnes or presence_bateau((pos[0] + i, pos[1]), flotte)):
                return False

    if (orientation == 'h'):
        pos_s = [(pos[0], pos[1] + i) for i in range(taille)]
        for i in range(taille):
            if (pos[1] + i not in ycolonnes or presence_bateau((pos[0], pos[1] + i), flotte)):
                return False
    flotte.append({"nom": nom, "taille": taille, "cases touchés": 0, "positions": pos_s})
    return True

def presence_bateau(pos, flotte):
    """Fonction qui vérifie si un bateau est présent à la position pos"""
    for f in flotte:
        if (pos in f["positions"]):
            return True
    return False

def plot_flotte_grid(m, flotte):
    """Fonction qui affiche la grille avec les bateaux """
    S = "  "
    S = S + " ".join(COLONNES)
    S = S + "\n"
    for i in range(N):
        S = S + LIGNES[i + 1] + " "
        for j in range(N):
            if presence_bateau((i, j), flotte) and m[i][j]!=TOUCHE:
                S = S + BATEAU + " "
            else:
                S = S + m[i][j] + " "
        S = S + "\n"
    print(S)

def input_ajout_bateau(flotte, nom, taille):
    """Fonction qui ajoute les bateaux sur la grille de jeu"""
    Spos = input("Merci de choisir une position : ")
    while search(r"[a-z]{1}\s{1}[0-9]{1}",Spos)==None:
        print("position non valide")
        Spos=input("Veuillez entrer une nouvelle position: ")
    pos = pos_from_string(Spos)
    orientation = input("Merci de choisir une orientation (h ou v) : ")
    while (orientation != "h" and orientation != "v"):
        print("entrée non valides")
        orientation = input("Merci de re-choisir une orientation (h ou v) : ")
    while (nouveau_bateau(flotte, nom, taille, pos, orientation) == False):
        print("Oups! nous pouvons ajouter le nouveau bateau !")
        Spos = input("Merci de choisir une position : ")
        while search(r"[a-z]{1}\s{1}[0-9]{1}",Spos)==None:
            print("position non valide")
            Spos=input("Veuillez entrer une nouvelle position: ")
        pos = pos_from_string(Spos)
        orientation = input("Merci de choisir une orientation (h ou v) : ")
        while (orientation != "h" and orientation != "v"):
            print("entrée non valides")
            orientation = input("Merci de choisir une orientation (h ou v) :")

def init_joueur():
    """Fonction ajoute les bateaux du joueur"""
    flotte = []
    m = create_grid()
    for i in range(len(NOMS)):
        print("Merci de saisir les informations du bateau " + NOMS[i] + " de taille : " + str(TAILLES[i]))
        input_ajout_bateau(flotte, NOMS[i], TAILLES[i])
        plot_flotte_grid(m, flotte)
    return m, flotte

def init_ia():
    """Fonction qui ajoute les bateaux de l'IA"""
    flotte = []
    m = create_grid()
    for i in range(len(NOMS)):
        pos = random_position()
        if (randrange(0, 200) % 2 == 0):
            orientation = "h"
        else:
            orientation = "v"
        while (nouveau_bateau(flotte, NOMS[i], TAILLES[i], pos, orientation) == False):
            pos = random_position()
            if (randrange(0, 200) % 2 == 0):
                orientation = "h"
            else:
                orientation = "v"
    return m, flotte

def tour_ia_random(m, flotte):
    """Fonction qui s'occupe du tour de l'IA pour les tirs"""
    pos = random_position()
    while m[pos[0]][pos[1]] != VIDE:
        pos = random_position()
    tir(m, string_from_pos(pos), flotte)
    return ""

def tour_joueur(nom, m, flotte):
    """Fonctio qui demande au joueur le coordonnées de tirs"""
    pos = input("Veuillez rentrer une poition pour tirer (de la forme 'ligne colonne') :")

    while search(r"[a-z]{1}\s{1}[0-9]{1}",pos)==None:
        print("position non valide")
        pos=input("Veuillez entrer une nouvelle position: ")
    p = pos_from_string(pos)
    while m[p[0]][p[1]] != VIDE:
        print("Case déjà attaquée!")
        pos = input(" Veuillez rentrer une autre position: ")
        while search(r"[a-z]{1}\s{1}[0-9]{1}",pos)==None:
            print("position non valide")
            pos = input("Veuillez entrer une nouvelle position: ")
        p = pos_from_string(pos)
    tir(m, pos, flotte)
    return ""

def tour_ia_better_random(m,flotte):
    """Fonction qui améliore la capacité de tir de l'IA"""
    k=0
    for i in range(len(flotte)):
        if flotte[i]["cases touchés"]>0 and flotte[i]["cases touchés"]!=flotte[i]["taille"]:
            k+=1
    if k>0:
        for x in range(len(m)):
            for y in range(len(m[x])):
                if m[x][y]==TOUCHE:
                    if x>0:
                        if m[x-1][y] == VIDE:
                            tir(m,string_from_pos((x-1,y)),flotte)
                            return ""
                    elif y>0:
                        if m[x][y-1] == VIDE:
                            tir(m,string_from_pos((x,y-1)),flotte)
                            return ""
                    elif x<9:
                        if m[x+1][y] == VIDE:
                            tir(m,string_from_pos((x+1,y)),flotte)
                            return ""
                    elif y<9:
                        if m[x][y+1] == VIDE:
                            tir(m,string_from_pos((x,y+1)),flotte)
                            return ""
    tir(m,string_from_pos(random_position()),flotte)
    return ""

def string_from_pos(s):
    """Fonction qui transforme les coordonnées en chaine de caractère"""
    l = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    c = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    x=[l[s[0]],str(c[s[1]])]
    return " ".join(x)

def id_bateau_at_pos(pos, flotte):
    """Fonction qui renvoie la position du bateau dans la flotte"""
    if presence_bateau(pos, flotte) == True:
        for i in range(len(flotte)):
            if presence_bateau(pos,[flotte[i]]):
                return i
    else:
        return ""

def test_fin_partie(nom, m, flotte, nb_tour):
    """Fonction qui teste si la parti est finie"""
    if flotte == []:
        print("Le joueur", nom, "a gagné après ", nb_tour, "coups")
        exit()


def joueur_vs_ia():
    """Fonction qui s'occupe du jeu entre un joueur et l'IA """
    nb_tour = 1
    m1, flotte1 = init_ia()
    nom1=input("quel est votre nom: ")
    hide(50)
    m2, flotte2 = init_joueur()
    hide(50)
    nom2="IA"
    while not test_fin_partie(nom1, m1, flotte1, nb_tour) or not test_fin_partie(nom2, m2, flotte2, nb_tour):
        print(color.BLUE + "Votre grille :" + color.RESET)
        plot_flotte_grid(m2, flotte2)
        tour_joueur(nom1, m1, flotte1)
        hide(2)
        if flotte1 == []:
            test_fin_partie(nom1, m1, flotte1, nb_tour)
        input("Appuyer sur entrer pour passer au tour de l'adversaire")
        hide(50)
        print("tir adverse :")
        tour_ia_random(m2, flotte2)
        hide(2)
        input("Appuyer sur entrer pour passer à votre tour")
        hide(50)
        nb_tour += 1

def hide(x):
    """Fonction qui cache l'affichage"""
    for i in range(x):
        print(" ")

def deux_joueurs():
    """Fonction qui s'occupe du jeu joueur contre joueur"""
    nb_tour = 1
    nom1 = input("Nom joueur 1: ")
    nom2 = input("Nom joueur 2: ")
    hide(50)
    print(nom1 + " placer vos bateau")
    m1, flotte1 = init_joueur()
    hide(50)
    print(nom2 + " placer vos bateau")
    m2, flotte2 = init_joueur()
    hide(50)
    while not test_fin_partie(nom2, m2, flotte2, nb_tour) or not test_fin_partie(nom1, m1, flotte1,nb_tour):
        print("Votre grille :")
        plot_flotte_grid(m1, flotte1)
        print(color.BLUE + nom1 + color.RESET + " à vous de jouer !")
        tour_joueur(nom1, m2, flotte2)
        hide(2)
        if flotte2 == []:
            test_fin_partie(nom2, m2, flotte2, nb_tour)
        input("Appuyer sur entrer pour passer au tour de " + nom2)
        hide(50)
        print("Votre grille :")
        plot_flotte_grid(m2, flotte2)
        print(color.RED + nom2 + color.RESET + " à vous de jouer !")
        tour_joueur(nom2, m1, flotte1)
        hide(2)
        input("Appuyer sur entrer pour passer au tour de " + nom1)
        hide(50)
        nb_tour += 1

#BONUS IA VS IA
def ia_vs_ia():
    """Fonction qui s'occupe du jeu entre IA """
    nb_tour = 1
    m1, flotte1 = init_ia()
    plot_flotte_grid(m1, flotte1)
    nom1 = "IA_1"
    m2, flotte2 = init_ia()
    plot_flotte_grid(m2, flotte2)
    nom2 = "IA_2"
    while not test_fin_partie(nom1, m1, flotte1, nb_tour) or not test_fin_partie(nom2, m2, flotte2, nb_tour):
        if flotte1 == []:
            test_fin_partie(nom1, m1, flotte1, nb_tour)
        print("tir " + nom2)
        tour_ia_random(m2, flotte2)
        plot_flotte_grid(m2, flotte2)
        nb_tour += 1
        if flotte2 == []:
            test_fin_partie(nom2, m2, flotte2, nb_tour)
        print("tir " + nom1)
        tour_ia_random(m1, flotte1)
        plot_flotte_grid(m1, flotte1)
        nb_tour += 1

#BONUS LEVEL UP IA
def joueur_vs_ia_level_up():
    """Fonction qui s'occupe du jeu entre un joueur et l'IA """
    nb_tour = 1
    m1, flotte1 = init_ia()
    nom1 = input("quel est votre nom: ")
    hide(50)
    m2, flotte2 = init_joueur()
    hide(50)
    nom2 = "IA"
    while not test_fin_partie(nom1, m1, flotte1, nb_tour) or not test_fin_partie(nom2, m2, flotte2, nb_tour):
        print(color.BLUE + "Votre grille :" + color.RESET)
        plot_flotte_grid(m2, flotte2)
        tour_joueur(nom1, m1, flotte1)
        hide(2)
        if flotte1 == []:
            test_fin_partie(nom1, m1, flotte1, nb_tour)
        input("Appuyer sur entrer pour passer au tour de l'adversaire")
        hide(50)
        print("tir adverse :")
        tour_ia_better_random(m2, flotte2)
        hide(2)
        input("Appuyer sur entrer pour passer à votre tour")
        hide(50)
        nb_tour += 1

def ia_vs_ia_level_up():
    """Fonction qui s'occupe du jeu entre IA """
    nb_tour = 1
    m1, flotte1 = init_ia()
    plot_flotte_grid(m1, flotte1)
    nom1 = "IA_1"
    m2, flotte2 = init_ia()
    plot_flotte_grid(m2, flotte2)
    nom2 = "IA_2"
    while not test_fin_partie(nom1, m1, flotte1, nb_tour) or not test_fin_partie(nom2, m2, flotte2, nb_tour):
        if flotte1 == []:
            test_fin_partie(nom1, m1, flotte1, nb_tour)
        print("tir " + nom2)
        tour_ia_better_random(m2, flotte2)
        plot_flotte_grid(m2, flotte2)
        nb_tour += 1
        if flotte2 == []:
            test_fin_partie(nom2, m2, flotte2, nb_tour)
        print("Votre grille :")
        print("tir " + nom1)
        tour_ia_better_random(m1, flotte1)
        plot_flotte_grid(m1, flotte1)
        nb_tour += 1

def jouer():
    """Fonction qui commence le jeu avec 1 ou 2 joueurs"""
    n = int(input("Veuillez chosir le mode de jeu ! \n"
                  "(0) joueur \n"
                  "(1) joueur contre l'IA \n"
                  "(2) joueurs \n"))
    while n != 1 and n != 2 and n != 0:
        n = int(input("Veuillez chosir 1 ou 2 joueur ou 0 pour un match entre ia : "))
    hide(50)
    if n == 1:
        niv = int(input("Veuillez choisir un niveau de difficulté ! \n"
                        "(1) Facile \n"
                        "(2) Difficile \n"))
        while niv != 1 and niv != 2:
            niv = int(input("Veuillez entrer 1 (niveau facile) ou 2 (niveau difficile) : "))
        hide(50)
        if niv == 1:
            joueur_vs_ia()
        else:
            joueur_vs_ia_level_up()

    if n == 0:
        niv = int(input("Veuillez choisir un niveau de difficulté ! \n"
                        "(1) Facile \n"
                        "(2) Difficile \n"))
        while niv != 1 and niv != 2:
            niv = int(input("Veuillez entrer 1 (niveau facile) ou 2 (niveau difficile) : "))
        hide(50)
        if n == 1:
            ia_vs_ia()
        else:
            ia_vs_ia_level_up()
    else:
        deux_joueurs()

jouer()