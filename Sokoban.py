# # # # #  Imports # # # # # # # # # # # # # # # # # # # # # # 

from upemtk import *
from random import choice
from os import listdir
from Menu_Final import *
from FonctionCommunes import *

# # # # #  Constantes utilisee pour le jeu # # # # # 

# Décalage pour laisser la place au titre dans les dimensions de la fenetre
decalage = 2
taille_case = 60
# Dico pour toutes les variable que je veux globaliser pour eviter d'avoir à les emporter dans les fonction en tant que paramètre
dico_variables = {"cle"         : 0,
                  "deplacement" : 0,
                  "gardien"     : None,
                  "debug"       : False,
                  "tirer"       : False,
                  "quitter"     : False,
                  }
                  
# Dico pour comptabiliser les positions des targets et des clés pour la vérification de ses dernières
# Pour les clés, je vais utiliser deux liste, une qui réfère les position des clés, et une autre pour la méthode de notation pour vérifier qu'elle clés à été prise tout en gardant leurs position enregistrer
dico_TargetKey = {"T" : [],
                  "K" : ([], []),
                  }

# Dico pour la taille de la fenetre et le titre, pour les mêmes raison que le dico_variable
dico_fenetre = {"titre"  : None,
                "largeur": 0,
                "hauteur": 0,
                }
                
                
# # # # # #  Fonctions # # # # # # # # # # # # # # # # # # # # # # # # # # 

def LireFichier(fichier, sets = ''):
    '''
    Cette fonction à deux utilités:
    
        -Récupérer les informations du fichier save pour la recharge de la map, dans ce cas on renvoie la matrice de jeu, le calque et les infos complémentaires
    
        -Récupérer la map d'un fichier et d'en faire la matrice de jeu, dans ce cas on renvoie la matrice de jeu
    
    fichier est la variable donné pour le nom du fichier qui contient la map,
    sets = '' est pour le chargement d'une carte, si il vaut autre chose comme "save" alors, c'est pour le chargement de la sauvegarde
    '''
    
    with open(fichier) as f:
        
        mat_jeu = []
            
        # Up de la map
        if sets == '':
            
            # On split les lignes et on récupère le titre en le supprimant de la liste
            txt = f.read().split("\n")[:-1]
            dico_fenetre["titre"] = txt.pop(0).split(":")[1].replace('"', "").strip()
            
            # On transtype la matrice
            for ligne in txt:
                mat_jeu.append(list(ligne))
        
            return mat_jeu
        
        # Sauvegarde
        else:
            
            # On split les paragraphes d'infos
            txt = f.read().split("\n\n")
            dico_fenetre["titre"] = txt.pop(0).split(":")[1].replace('"', "").strip()   # On récupere le titre en enlevant les espaces et les guillemets, supprimé de la liste
            
            # On attribut les paragraphes à leurs définition respectives
            mat = txt[0].split("\n")
            calc = txt[1].split("\n")
            Info = txt[2].split("\n")
            
            
            # On transtype la matrice, le calque et les infos
            for ligne in mat:
                mat_jeu.append(list(ligne))
            
            calque = []
            for ligne in calc:
                calque.append(list(ligne))
            
            for i in range(len(Info)):
                # Si on récupère les informations des clés prises
                if i == 4:
                    cles = []
                    for elt in Info[i]:
                        if elt == '0' or elt == '1':
                            cles.append(int(elt))
                    
                    dico_TargetKey["K"] = (dico_TargetKey["K"][0], cles)
                else:
                    Info[i] = int(Info[i])
            
            return mat_jeu, calque, Info
        
    
def creer_calque_jeu(M):
    '''
    Création d'un calque ne prenant que les targets et les clés (Explication de la raison de cette matrice dans le README)
    
    M: Matrice_jeu
    '''
    m, p = len(M), len(M[0])
    calque=[]
    dico_TargetKey["T"], dico_TargetKey["K"] = [], ([], [])
    
    # On change toutes les éléments autres que les targets et les clés en case vide
    for i in range(m):
        ligne=[]
    
        # Pour chaque clés et target, on met leurs position dans la matrice dans les dico, cela servira pour la fonction check_calque
        for j in range(p):
            if M[i][j] == 'T':
                ligne.append(M[i][j])
                dico_TargetKey["T"].append((i,j))
                
            elif M[i][j] == 'K':
                ligne.append(M[i][j])
                dico_TargetKey["K"][0].append((i,j))
                dico_TargetKey["K"][1].append(1)
            else:
                ligne.append('.')
    
        calque.append(ligne)
        

    return calque
    
def affiche_jeu(M, calque, sets = 1, decalage = 0):
    '''
    Affiche la matrice jeu, le titre ainsi que la matrice calque. 
    Elle va également permettre de modifer la matrice de jeu, pour y supprimer les éléments de la matrice calque.
    Enfin, elle va renvoyer la position du gardien pour garder sa position dans la matrice.
    
    M : Matrice jeu
    calque : Matrice calque
    sets : Si il n'est pas spécifier, la fonction va seulement afficher
    decalage: c'est le décalage de l'affichage de la matrice, si la matrice est trop petite pour la fenetre, on l'ajuste pour qu'elle soit centré
    '''
    m,p = len(calque), len(calque[0])
    
    # Si la matrice est trop petite, on l'ajuste
    if dico_fenetre["largeur"] == 540:
        decalage = (9 - p) // 2
    
    # Affichage des compteurs
    NbK = 'Clés : {}'.format(dico_variables["cle"])
    NbAction = 'Actions : {}'.format(dico_variables["deplacement"])
    
    
    texte(12,2, dico_fenetre["titre"] ,"black","nw","Dejavu")               # Titre
    texte(12,70, NbK,"black","nw","Dejavu")                                 # Nombre de clés
    texte(dico_fenetre["largeur"]-12,70, NbAction,"black","ne","Dejavu")    # Nombre d'action
    if dico_variables["debug"]:
        texte(dico_fenetre["largeur"]-12,2,"Debug","green", "ne", "Dejavu") # Debug activé
    else:
        texte(dico_fenetre["largeur"]-12,2,"Debug","red", "ne", "Dejavu")   # Debug desactivé
        
    if dico_variables["tirer"]:
        texte(dico_fenetre["largeur"]-175,2,"Tirer","green","ne","Dejavu")  # Tirer activé
    else:
        texte(dico_fenetre["largeur"]-175,2,"Tirer","red","ne","Dejavu")    # Tirer désactivé

    
    # On affiche la matrice calque
    affiche_calque_jeu(calque, decalage)
    
    # On affiche la matrice de jeu en changant les target et les clés en case vide, et en prélevant les coordonnées du gardien
    for i in range(m):
    
        for j in range(p): 
            
            if M[i][j] == 'S':
                # Récupératiion de la position du gardien
                dico_variables["gardien"] = (i,j)
                
            
            elif M[i][j] == 'T' or M[i][j] == 'K':
                # Changement des targets et clés en cases vides
                M[i][j] = '.'
    
            affiche_case(i, j, M[i][j], decalage)
        
def affiche_calque_jeu(calque, decalage):
    '''
    Affiche la matrice calque
    
    calque : Matrice calque
    decalage: On applique le decalage donné à la fonction précédente
    '''
    m, p = len(calque), len(calque[0])
    
    for i in range(m):
    
        for j in range(p):
            affiche_case(i, j, calque[i][j], decalage)


def deplace_gardien(M, direction):
    '''
    Fonction pivot qui va permettre la vérification du mouvement et veiller à son application.
    
    M: Matrice de jeu
    direction: Direction donnée par le joueur
    
    Note importante: On considère que si la variable inv_Gb est établi à None, alors le mode tirer est désactiver
    '''
    G = dico_variables["gardien"]
    
    # Au cas ou le mode tirer est désactiver, si inv_Gb est établi à None, on considère que le mode tirer est désactiver, sinon il est modifier plus tard
    inv_Gb = None
    
    
   
    if direction == 'Left': 
        direction = (0,-1)
        
    elif direction == 'Right':
        direction = (0,1)
        
    elif direction == 'Up': 
        direction = (-1,0)
        
    elif direction == 'Down':
        direction = (1,0)
        
    else:
        return None
        
    # prochaine position du gardien
    Gb = G[0] + direction[0], G[1] + direction[1]
    
    # Si le gardien pousse une caisse, on regarde la prochaine position de la caisse
    dGb = Gb[0] + direction[0], Gb[1] + direction[1]
    
    # Si le mode tirer est activé, on regarde la case qui est à l'inverse de la direction (Si le joueur donne gauche, on regarde la case à droite)
    
    if dico_variables["tirer"] == True:
        inv_Gb = G[0] + direction[0]*-1, G[1] + direction[1]*-1
    
    # On vérifie si on peut effectuer le déplacement
    move = moveOK(Gb,dGb,M, inv_Gb)
    
    # On effectue le mouvement en fonction de la verification
    effectue_move(M, move, G, Gb, dGb, inv_Gb)
    
    
    
def moveOK(Gb, dGb, M, inv_Gb):
    '''
    Détermine si un déplacement va pouvoir être effectuer ou non. 
    On renvoie False si le déplacement n'est pas possible,
    sinon on renvoie la case sur laquelle il va se deplacer
    
    M: Matrice de jeu
    Gb: Gardien bouge, prochaine position du gardien
    dGb: Deuxième gardien bouge, Dans la mesure ou le gardien déplace une caisse, on regarde la prochaine position de la caisse
    inv_Gb: Inverse gardien bouge, regarde la case derrière le gardien
    '''

    # Si le mode tirer est activer, on regarde que le gardien ne cherche pas tirer en dehors de la matrice de jeu
    if inv_Gb is not None:
        if inv_Gb[0] > len(M)-1 or inv_Gb[1] > len(M[0])-1 or inv_Gb[0] < 0 or inv_Gb[1] < 0:
            # Si le gardien tire en dehors de la matrice, on désactive le mode tirer
            dico_variables["tirer"] = False
    
    # On vérifie que le gardien ne sorte pas de la dico_fenetre["carte"]
    if Gb[0]>len(M)-1 or Gb[1]>len(M[0])-1 or Gb[0]<0 or Gb[1] < 0:
        return False

    # On vérifie si la prochaine case est vide
    elif M[Gb[0]][Gb[1]] == '.':
        return '.'
        
    # On vérifie si la prochaine case  est une caisse
    elif M[Gb[0]][Gb[1]] == 'B':
        # Si la caisse va sortir, on return False
        
        if dGb[0]>len(M)-1 or dGb[1]>len(M[0])-1 or dGb[0] < 0 or dGb[1] < 0:
            return False
        
        # Si c'est une caisse, on vérifie que la case après est vide
        if M[dGb[0]][dGb[1]] == '.':
            return 'B'

    # On vérifie si la prochaine case est une porte
    elif M[Gb[0]][Gb[1]] == 'D':
        return 'D'
    
    return False

def effectue_move(M, move, G,  Gb, dGb, inv_Gb):
    '''
    Effectue le déplacement autoriser par la fonction moveOK
    
    M: Matrice de jeu
    Move: Déplacement à effectuer
    G: Position du gardien
    Gb: Prochaine position du gardien
    dGb: Prochaine position de la caisse
    Inv_Gb : Position de la caisse à tirer
    
    On considère que le gardien ne peut ouvrir une porte ou pousser une 
    caisse en même temps que de tirer une caisse
    
    A la fin de chaque déplacement, on active la fonction dplcmt, elle va permettre d'actualiser le compteurs de déplacement
    '''
    # Déplacement du gardien sur une case vide
    if move == '.':
        M[G[0]][G[1]], M[Gb[0]][Gb[1]] = M[Gb[0]][Gb[1]], M[G[0]][G[1]]
        
        # Si devant lui, le gardien à une case vide, il peut tirer une caisse, si le mode est activer et qu'il y a une caisse derrière lui
        if dico_variables["tirer"]:
            if M[inv_Gb[0]][inv_Gb[1]] == 'B':
                M[inv_Gb[0]][inv_Gb[1]], M[G[0]][G[1]] = M[G[0]][G[1]], M[inv_Gb[0]][inv_Gb[1]]
                
            else:
                dico_variables["tirer"] = False
        
        IncAction()
        
    # Déplacement du gardien sur une porte
    if move == 'D':
        if compteur_keys():
            M[Gb[0]][Gb[1]] = '.'
            M[G[0]][G[1]], M[Gb[0]][Gb[1]] = M[Gb[0]][Gb[1]], M[G[0]][G[1]]
            
            IncAction()
            
    
    
    # Déplacement du gardien sur une caisse
    if move == 'B':
        M[Gb[0]][Gb[1]], M[dGb[0]][dGb[1]] = M[dGb[0]][dGb[1]], M[Gb[0]][Gb[1]]
        M[G[0]][G[1]], M[Gb[0]][Gb[1]] = M[Gb[0]][Gb[1]], M[G[0]][G[1]]
        dico_variables["tirer"] = False
        
        IncAction()
        
        
def compteur_keys(sets = 0):
    '''
    Fonction qui va augmenter le compteur si le joueur ramasse une clé. Elle va également servir à confirmer le déplacement sur une porte en fonction des keys que possède le joueur
    
    sets: 
        -Si il n'est pas spécifier, vérifie si le joueur peut ouvrir une porte
        -Si il vaut 1, ajoute une clé dans le compteur de clé
    '''
    if sets == 1:
        dico_variables["cle"] += 1
        # affiche le nouveau compteur
        return None
        
    else:
        # Si le compteur n'est pas à 0, on lui retire 1 key, et renvoie que le gardien peut se déplacer
        if dico_variables["cle"] != 0:
            dico_variables["cle"] -= 1
            return True
        # Sinon, on renvoie que le gardien ne peut pas se déplacer
        return False
   
def check_calque(M,calque):
    '''
    Elle repère si toutes les caisses sont sur les targets, pour activer la victoire
    sinon, elle repère si le joueur à récupérer une clé.
    Renvoie False si le joueur n'a pas gagné, True si il à gagné.
    
    M: Matrice de jeu
    calque: Matrice calque
    '''
    m,p = len(M), len(M[0])
    RamK = None
    
    # On fait attention à ce que la carte possède des clés
    if any(dico_TargetKey["K"][1]):
        ind = len(dico_TargetKey["K"][0]) - 1
        # On va du nombre de clés actuelle et on descend jusqu'a 0
        while ind != -1:
            if dico_TargetKey["K"][1][ind] == 1:
                i,j = dico_TargetKey["K"][0][ind]
                
                if M[i][j] == "S":
                    # On ajoute une clé
                    compteur_keys(1)
                    # On remplace la clé prise par une case vide
                    calque[i][j] = '.'
                    # On change l'état de la clés pour indiquer qu'on ne doit plus la regarder
                    dico_TargetKey["K"][1][ind] = 0
                
            ind -= 1
    
    # On vérifie toutes les positions des targets, si il n'y a pas de caisse, on return False
    for coupleTarget in dico_TargetKey["T"]:
        i,j = coupleTarget
        if M[i][j] != "B":
            return False
    
    return True
    
def affiche_victoire():
    '''
    Affichage de victoire
    '''
    dico_variables["quitter"], dico_variables["cle"], dico_variables["deplacement"] = True, 0, 0
    avertissement(dico_fenetre["hauteur"], dico_fenetre["largeur"], "Bravo ! Vous avez gagné !",1)

def reset(fichier, calque):
    """
    Réinitialise le jeu 
    Renvoie la nouvelle matrice de jeu, le nouveau calque, le titre, et la  nouvelle position du gardien.
    
    fichier: Nom du fichier
    calque: Matrice calque
    
    On va reset la carte en réouvrant la carte comme si on lançait le jeu.
    """
    
    Matrice_jeu = LireFichier("Map/" + fichier)
    calque = creer_calque_jeu(Matrice_jeu)
    affiche_jeu(Matrice_jeu, calque, 0)
    dico_variables["cle"] = 0
    dico_variables["deplacement"] = 0
    
    return Matrice_jeu, calque

def DebugMode(sets = None):

    """
    Fonction qui inverse l'état de la variable debug (True/False).
    Renvoie une direction aléatoire une direction si le debug est True
    
    sets:
        -Si n'est pas spécifié, considère que le debug mode est activé et renvoie une direction aléatoire
        -Si vaut 0, désactive / active le mode debug
    """
    # On inverse la variable
    if sets == "switch":
        dico_variables["debug"] = not dico_variables["debug"]
    
    direction = ["Left","Right","Up","Down"]
    direction = choice(direction)
    
    return direction

def ModeTirer():
    """
    Inverse le mode tirer.
    
    Tirer: False ou True, si le mode tirer est activé ou non.
    """
    dico_variables["tirer"] = not dico_variables["tirer"]
    IncAction()

def event(Matrice_jeu, calque):
    """
    Fonction qui sert d'interface à l'application des contrôles donnés par le joueur.
    On récupère les contrôle grâce à une fonction.
    On renvoie la direction, la nouvelle matrice de jeu, la nouvelle matrice calque, le titre, la noivealle position du gardien,
    les variables debug et tirer
    
    Matrice_jeu: Matrice de jeu
    calque: Matrice calque
    titre: Titre de la map
    gardien: Position du gardien
    debug: False ou True, si le mode debug est activer ou non
    tirer: False ou True, si le mode tirer est activer ou non.
    """
    # On récupère les contrôles du joueur
    touche = Controles()
    
    
    # # # # # # # # # # # # # # #  FERMETURE DU JEU # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    
    if touche == 'Escape':
        if avertissement(dico_fenetre["hauteur"], dico_fenetre["largeur"], "Voulez-vous save en quittant ?"):
            sauvegarde(Matrice_jeu, calque)
        
        dico_variables["quitter"], dico_variables["cle"], dico_variables["deplacement"] = True, 0, 0
    # # # # # # # # # # # # # # #  ACTIVATION DU RESET # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    
    if touche == 'r':
        if avertissement(dico_fenetre["hauteur"], dico_fenetre["largeur"], "Etes-vous sûr de vouloir reset ?"):
            Matrice_jeu, calque = reset(dico_fenetre["carte"], calque)

    # # # # # # # # # # # # # # #  SAUVEGARDE DE LA MAP # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    
    if touche == 's':
        sauvegarde(Matrice_jeu, calque)
        
    # # # # # # # # # # # # # # #  RECHARGE DE LA MAP # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        
    if touche == 'l':
        if dico_fenetre["carte"] + "_save" in listdir("Saves"):
            if avertissement(dico_fenetre["hauteur"], dico_fenetre["largeur"], "Charger la sauvegarde ?"):
                # Chargement des sauvegardes
                Matrice_jeu, calque, infos = LireFichier("Saves/" + dico_fenetre["carte"] + "_save", "save")
                # La variable infos est une liste, chaque elt de la liste renvoie à une information
                
                
                dico_variables["gardien"]    = (infos[0],infos[1])
                dico_variables["cle"]         = infos[2]
                dico_variables["deplacement"] = infos[3]
    
    # # # # # # # # # # # # # # #  TIRER # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    if touche == 'Shift_L' or touche == 'Shift_R':
        ModeTirer()
    
    
    # # # # # # # # # # # # # # #  DEBUG # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    if touche == 'd':
        # Inverse le debug mode
        DebugMode("switch")
    
    # # # # # # # # # # # # # # #  RENVOIE DU DEPLACEMENT # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    
    if dico_variables["debug"] == True:
        # On affiche que le mode debug est activé
        # Renvoie une direction aléatoire
        direction = DebugMode()
        
        return direction, Matrice_jeu, calque
    
    
    if dico_variables["debug"] == False:
        if touche == 'Right':
            return 'Right', Matrice_jeu, calque
        elif touche == 'Left':
            return 'Left', Matrice_jeu, calque
        elif touche == 'Up':
            return 'Up', Matrice_jeu, calque
        elif touche == 'Down':
            return 'Down', Matrice_jeu, calque

            
    return 'RAS', Matrice_jeu, calque


    
def sauvegarde(Matrice_jeu, calque):
    """
    Permet la sauvegarde de la carte dans un fichier en quatre parties, une pour le titre, une pour la matrice jeu,
    une pour la matrice calque et une derniere pour toutes les informations complémentaire.
    Les fichiers s'appelleront "NomdelaCarte_NomdelaSauvegarde_save"
    
    Matrice_jeu: Matrice de jeu
    calque: Matrice calque
    
    A part la partie Infos, les matrice seront sauvegarder de la même manière qu'un fichier de carte.
    L'objectif étant que lors du chargement, on puisse utiliser la fonction lecture de fichier 
    pour lire les sauvegarde. 
    Cela nous permet alors de sauvegarder, de quitter le jeu puis de charger la sauvegarde de la carte.
    """
    m,p = len(calque), len(calque[0])
    x,y =  dico_variables["gardien"]
    
    # Sauvegarde de la Matrice_jeu sous la même forme qu'un fichier dico_fenetre["carte"]
    with open("Saves/"+dico_fenetre["carte"]+'_save', 'w') as f:
        
        for i in range(m):
            # On met le titre dans le fichier
            if i==0:
                f.write("Titre" + ':' + dico_fenetre["titre"] + "\n\n")
            # Ajoute un retour à la ligne en fin de ligne
            else:
                f.write("\n")
            
            for j in range(p):
                f.write(Matrice_jeu[i][j])
        
        f.write("\n\n")
        
        
        # Sauvegarde de la matrice calque
        for i in range(m):
            if i > 0:
                f.write("\n")
            
            for j in range(p):
                f.write(calque[i][j])
                
        f.write("\n")
        
        
        # Sauvegarde des informations complémentaire
        liste_info = [x, y, dico_variables["cle"], dico_variables["deplacement"], dico_TargetKey["K"][1]]
        
        for i,elt in enumerate(liste_info):
            
            f.write("\n" + str(elt))
        
        avertissement(dico_fenetre["hauteur"], dico_fenetre["largeur"], "Sauvegarde effectuée !", 1)
        
def IncAction():
    """
    Va servir à incrémenter le compteur de déplacement.
    """
    
    dico_variables["deplacement"] += 1
    
def Jeu():
    '''
    Fonction qui va accuillir la boucle du jeu, l'utilité de cette fonction est 
    d'allégé le main. Ensuite nous avons rajouter une boucle infinie pour 
    relancer le jeu dès que l'on quitte une carte ou alors le mode d'édition.
    La variable quitter du dico_variable va nous aider à gérer ce cas
    '''
    while True:
        #  Initialisation -----------------------------------------------
        cree_fenetre(1000, 750)
        # Choix de la carte
        dico_fenetre["carte"] = menu()
        
        ferme_fenetre()
        
        # Prise du fichier et initialisation de la matrice
        Matrice_jeu = LireFichier("Map/" + dico_fenetre["carte"])         
        
        # Initialisation de la fenetre en fonction du fichier
        
        dico_fenetre["largeur"] = len(Matrice_jeu[0]) * taille_case
        dico_fenetre["hauteur"] = (len(Matrice_jeu) + 2)* taille_case
        if dico_fenetre["largeur"] < 540:
            dico_fenetre["largeur"] = 540
        cree_fenetre(dico_fenetre["largeur"], dico_fenetre["hauteur"])
        
        # Création de la matrice calque
        calque = creer_calque_jeu(Matrice_jeu)
        
        # Initialisation de l'affichage
        affiche_jeu(Matrice_jeu, calque, 0)
        
        while dico_variables["quitter"] != True:
                efface_tout()
                # On affiche le jeu, on récupère au passage la position de la sentinelle
                affiche_jeu(Matrice_jeu, calque)
                if check_calque(Matrice_jeu, calque):
                    affiche_victoire()
                    dico_fenetre["carte"] = None
                    break
                
                # Controle des event qui intéragissent avec : la direction, la matrice de jeu, la matrice calque, le titre, la position du gardien et la variable debug 
                direction, Matrice_jeu, calque = event(Matrice_jeu, calque)
                # Déplace le gardien en fonction de la direction donné par le joueur.
                deplace_gardien(Matrice_jeu, direction)
        
        dico_variables["quitter"] = False
        ferme_fenetre()
if __name__ == '__main__':
    Jeu()
