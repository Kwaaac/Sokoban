from upemtk import *
from os import listdir
from Editeur import *


'''
Module de Fonction Communes.

Puisque nous réutilisions des fonctions dans le jeu et dans l'editeur, nous avons
décidé de mettre les fonctions qu'ils partagaient dans un seul et même module pour
évite de devoir répéter ses fonctions.
'''

def avertissement(h,l,msg, reponse = 0):
    '''
    Fonction qui va faire apparaître au milieu de la fenetre un message d'avertissement
    auquel l'utilisateur va devoir répondre par oui ou non, ou bien juste appuyer sur une
    touche ou cliquer pour le faire disparaition
    
    h: hauteur de la fenetre
    l: largeur de la fenetre
    msg: message à afficher
    reponse: si il vaut, 0 alors on demande une réponse de l'utilisateur
        sinon, il suffit de cliquer ou d'appuyer sur une touche
    '''
    # On prend la valeur d'un texte *2 pour y ajouter le "O/N"
    hauteur = hauteur_texte() * 2
    
    # On prend la longueur du message pour l'encadrer correctement
    longeur = longueur_texte(msg)
    
    # On défini la taille pour le début du rectangle 
    l = (l - longeur) // 2
    h = (h - hauteur) // 2
    
    
    rectangle(l-10, h, l + longeur+10, h + hauteur+10, "red", "white", 4, tag = "avertissement")
    
    
    # Si on demande une réponse, on affiche le message et en dessous, on affiche "O/N"
    if reponse == 0:
        texte(l+longeur //2, h + hauteur // 3, msg, "black", "center", "Dejavu", tag = "avertissement")
        texte(l + longeur // 2, h + 30 +  hauteur // 2 , "O/N", "black", "center", "Dejavu", tag = "avertissement")
        
        # On attend la réponse de l'utilisateur, on récupère alors un False ou un True
        act = Controles_msg()
        
        # On efface le rectangle et les textes
        efface("avertissement")
        return act
    
    # Sinon, on affiche un message sans demande de réponse
    else:
        texte(l+longeur //2, h + 15 + hauteur // 3, msg, "black", "center", "Dejavu", tag = "avertissement")
        attente_clic_ou_touche()
        efface("avertissement")
        
def Controles_msg():
    '''
    Fonction qui va prendre les commandes de l'utilisateur pour la fonction avertissement
    Renvoie True ou False en fonction de la réponse de l'utilisateur,
    si il donne "oui", on renvoie True, si il donne "non", on renvoie False
    '''
    while True:
        ev = donne_evenement()
        type_ev = type_evenement(ev)
        
        if type_ev == "Touche":
            if touche(ev) == "o"or touche(ev) == "O":
                return True
            
            elif touche(ev) == "n" or touche(ev) == "N":
                return False
        mise_a_jour()
                
def Controles():
    '''
    Fonction qui va prendre les commandes de l'utilisateur pour la boucle principal du jeu
    '''
    
    ev = donne_evenement()
    type_ev = type_evenement(ev)

    if type_ev == "Touche":
        return touche(ev)

    mise_a_jour()
    
def Edition(m,p):
    '''
    Initialise une matrice vide ainsi que une liste d'édition
    
    m: Nombre de ligne dans la matrice
    p: Nombre de colonnes dans la matrice
    
    La seconde liste équivaut à une matrice d'édition:
    
    S: Spawn Gardien
    B: Box
    K: Key
    W: Wall
    T: Target
    D: Door
    P: Case vide (pour séparer les options d'édition avec les éléments)
    V: Valider la carte
    R: Reset la carte
    Q: Quitter l'éditeur
    '''
    
    return [["." for i in range(p)] for j in range(m)], ["S","B","K","W","T","D","P","V","R","Q"]
    

def affiche_case(i, j, etat, decalageH = 0, decalageV = 2, taille_case = 60):
    """
    Utilise la bibliothèque upemtk pour afficher la case correspondante à la Matrice_jeu
    i,j sont les positions de la case dans la matrice
    etat: l'état de la case donner (Target, Wall, Box...)
    decalageH: Décalage Horizontal, si la matrice est trop petite pour 
        la fenetre, on peut définir un décalage pour centrer la matrice
    decalageV: Decalage Vertical, il est initialiser à 2 car à cause du
        titre, nous devons afficher la matrice deux cases plus bas
    taille_case: On initie la taille des case à 60
    """
    # Application des décalages
    j = j+decalageH
    i = i+decalageV
    
    # Affichage d'un mur
    if etat == 'W':
        rectangle(j*taille_case, i*taille_case, j*taille_case+taille_case, i*taille_case+taille_case, 'gray19', 'gray19')
        
    # Affichage d'une case vide
    if etat == '.':
        rectangle(j*taille_case, i*taille_case, j*taille_case+taille_case, i*taille_case+taille_case, 'gray')
        
    # Affichage d'une Target 
    if etat == 'T':
        rectangle(j*taille_case, i*taille_case, j*taille_case+taille_case, i*taille_case+taille_case, 'blue', 'blue')
        rectangle(j*taille_case+5, i*taille_case+5, j*taille_case+taille_case-5, i*taille_case+taille_case-5, 'white', 'white')
        
    # Affichage d'une boite/caisse
    if etat == 'B':
        rectangle(j*taille_case, i*taille_case, j*taille_case+taille_case, i*taille_case+taille_case, 'gray')
        rectangle(j*taille_case+5, i*taille_case+5, j*taille_case+taille_case-5, i*taille_case+taille_case-5, 'blue', 'blue')
        
    # Affichage du gardien
    if etat == 'S':
        rectangle(j*taille_case, i*taille_case, j*taille_case+taille_case, i*taille_case+taille_case, 'gray')
        cercle(j*taille_case + taille_case//2, i*taille_case + taille_case//2, 20, 'yellow', 'yellow')
    
    # Affichage d'une cle 
    if etat == 'K':
        rectangle(j*taille_case, i*taille_case, j*taille_case+taille_case, i*taille_case+taille_case, 'gray')
        polygone([(j*taille_case + taille_case//2, i*taille_case + taille_case//4), (j*taille_case + taille_case*0.75, i*taille_case + taille_case//2),
        (j*taille_case + taille_case//2, i*taille_case + taille_case*0.75), (j*taille_case + taille_case*0.25, i*taille_case + taille_case//2)], 'green4', 'green4')
        
    # Affichage d'une porte
    if etat == 'D':
        rectangle(j*taille_case, i*taille_case, j*taille_case+taille_case, i*taille_case+taille_case, 'green4', 'green4')
        polygone([(j*taille_case + taille_case//2, i*taille_case + taille_case//4), (j*taille_case + taille_case*0.75, i*taille_case + taille_case//2), 
        (j*taille_case + taille_case//2, i*taille_case + taille_case*0.75), (j*taille_case + taille_case*0.25, i*taille_case + taille_case//2)], 'white', 'white')
    
    # Affichage vide pour afficher le titre de la carte ainsi que des informations complémentaires(clef, nbr de mouvement etc.)
    else:
        pass





