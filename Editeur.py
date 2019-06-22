from upemtk import *
import string as strg
from FonctionCommunes import *

'''
Module de l'Editeur
'''

# On défini un dico global pour le pointeur de la souris pour prendre en compte la sélection
Pointeur = {"bloc": ".",}

# On défini un dico global pour le nombre de target, de box etc. pour la fonction verif_carte_correcte
Compteur = {"T": 0,
            "B": 0,
            "S": 0,
            }

def verif_carte_correcte(h,l):
    '''
    On vérifie le dictionnaire Compteur pour vérifier que la map est valide
    
    h: Hauteur
    l: Largeur
    '''
    if Compteur["S"] != 1 or Compteur["B"] < Compteur["T"] or Compteur["T"] == 0:
        avertissement(h,l,"La carte n'est pas valide !", 1)
        return False
    
    Compteur["T"],Compteur["B"], Compteur["S"] = 0, 0, 0
    return True
    
def controle2():
    '''
    Fonction qui va prendre les commandes de l'utilisateur
    '''

    ev = donne_evenement()
    type_ev = type_evenement(ev)
    
    
    if type_ev == "Touche":
        
        # Si on appuis sur Entre
        if touche(ev) == "Return":
            return "go"
        
        # Si on appuis Retour
        elif touche(ev) == "BackSpace":
            return "eff"
        
        elif 'KP' in touche(ev):
            return touche(ev)[-1]
            
        return touche(ev)
        
    return ""
    
    
def demandeTaille():
    '''
    Fonction qui va prendre la taille de plateau au joueur
    '''
    entree= ""
    etape = 0
    
    while True:
        efface_tout()
        
        # Fond
        rectangle(0,0, 1000, 750, "black", "black")
        
        # On récupère les controles
        cont = controle2()
        
        # On vérifie que le nombre n'est pas trop grand et est un nombre, si oui, on l'ajoute
        if len(entree) < 2 and cont in strg.digits:
                entree += cont
        
        # Effacement
        if cont == "eff":
            entree = entree[:-1]
        
        # Si on demande la largeur
        if etape == 0:
            
            texte(500,750//3, "Donnez la largeur du plateau (max: 31)","red" , "center", "Dejavu")
            texte(500,750//3 + 150, "{}".format(entree),"white" , "center", "Dejavu")
            
            # Si le nombre n'est pas vide et que l'utilisateur entre la largeur
            if cont == "go" and entree != "":
                
                # On vérifie qu'il n'est pas mit 0 ou au dessus de la limite max
                if 0 < int(entree) < 32 :
                    
                    # On réinitialise l'entrée, on change d'étape
                    largeur = entree
                    etape += 1
                    entree = ""
                    
                # Sinon, on indique au joueur que le nombre fourni est incorrect
                else:
                    avertissement(750, 1000, "Largeur incorrect", 1)
                    entree = ""
        
        # Si on demande la hauteur
        elif etape == 1:
            texte(500,750//3, "Donnez la hauteur du plateau (max: 15)","red" , "center", "Dejavu")
            texte(500,750//3 + 150, largeur + "x{}".format(entree),"white" , "center", "Dejavu")
            
            if cont == "go" and entree != "":
                
                if 0 < int(entree) < 16:
                    hauteur = entree
                    Matrice_APP, Liste_EDIT = Edition(int(hauteur),int(largeur))
                    break
                    
                else:
                    avertissement(750, 1000, "Hauteur incorrect", 1)
                    entree = ""
                    
        mise_a_jour()
        
    ferme_fenetre()
    # On lance l'édition une fois la taille de la matrice récupérer
    Editeur(Matrice_APP, Liste_EDIT)
            
def Editeur(Matrice_APP, Liste_EDIT , decalage = 0, end = False, taille_case = 60):
    '''
    Fonction qui affiche l'editeur et permet l'edition d'une map
    
    Matrice_APP: La matrice d'application, c'est sur cette matrice vide que les éléments vont être ajouter
    Liste_Edit: Liste d'édition
    decalage: décalage dans le cas ou la matrice est trop petite pour la fenetre
    end: Initier à False, sert à sortir de la boucle et de terminer l'édition
    taille_case: taille des cases
    '''
    m,p = len(Matrice_APP), len(Matrice_APP[0])
    
    hauteur = m* taille_case + 2*taille_case
    largeur = p * taille_case
    
    # Decalage
    if largeur < 600:
       
        decalage = (10 - p) // 2
        
        largeur = 600
        
    cree_fenetre(largeur,hauteur)
    
    while end == False:
        # On récupère la position du clic dans la matrice
        x, y, mode, clic = attrCase(hauteur//60,largeur//60)
        
        # Si le joueur veut quitter le mode édition
        if Pointeur["bloc"] == "Q":
            
            Pointeur["bloc"] = "."
            if avertissement(hauteur,largeur, "Etes-vous sur partir ?"):
                Compteur["T"],Compteur["B"], Compteur["S"] = 0, 0, 0
                break
            
        # Si le joueur veut réinitialiser la map
        if Pointeur["bloc"] == "R":
            Pointeur["bloc"] = "."
            if avertissement(hauteur,largeur, "Etes-vous sur de reset ?"):
                Compteur["T"],Compteur["B"], Compteur["S"] = 0, 0, 0
                Matrice_APP, Liste_EDIT = Edition(m,p)
            
        # Si le joueur veut valider la map
        if Pointeur["bloc"] == "V":
            Pointeur["bloc"] = "."
            
            if verif_carte_correcte(hauteur, largeur):
                # Même chose que pour demander la taille du plateau
                entree = ""
                txt = "Nommez votre carte(max: 12 lettres)"
                
                while end == False:
                    efface_tout()
                    cont = controle2()
                    rectangle(0,0, largeur, hauteur, "black", "black")
                    
                    texte(largeur // 2, hauteur // 3, txt,"red" , "center", "Dejavu")
                    texte(largeur // 2, hauteur // 3 + 50, "{}".format(entree),"white" , "center", "Dejavu")
                                        
                    if cont in strg.ascii_letters or cont in strg.digits:
                        entree += cont
                    
                    elif cont == "eff":
                        entree = entree[:-1]
                    
                    # Mot trop court
                    elif cont == "go" and len(entree) == 0:
                        avertissement(hauteur, largeur, "Veuillez mettre un nom", 1)
                    
                    # Mot trop long
                    elif cont == "go" and len(entree) > 12:
                        msg = "Le nom est trop long({})".format(len(entree)-12)
                        avertissement(hauteur, largeur, msg, 1)
                    
                    # Sauvegarde du fichier
                    elif cont == "go" and 0 < len(entree) <= 12 :
                        with open("Map/"+entree, 'w') as f:
                            for i in range(m):
                                # On met le titre dans le fichier
                                if i==0:
                                    f.write("Titre" + ':' + entree)
                                    f.write("\n")
                            
                                # Ajoute un retour à la ligne en fin de ligne
                                for j in range(p):
                                    f.write(Matrice_APP[i][j])
                                    
                                f.write("\n")
                                    
                            Pointeur["bloc"] = '.'
                            end = True
                        
                    mise_a_jour()
        # Si le joueur clique sur l'édition
        if mode == "E":
                Pointeur["bloc"] = Liste_EDIT[x]
                
        efface_tout()
        image(0,0, "Image/Titre.png", "nw")
        
        # Pour le mode application
        for i in range(m):
            for j in range(p):
                if i == y-2 and j == x-decalage:
                    
                    # Si c'est un clic gauche, on applique
                    if clic == "ClicGauche" and mode == 'A':
                        
                        Matrice_APP[i][j] = Pointeur["bloc"]
                        
                        # On incrémente le compteur
                        if Pointeur["bloc"] in Compteur:
                            Compteur[Pointeur["bloc"]] += 1
                        
                    # Si c'est un clic droit, on supprime
                    if clic == "ClicDroit" and mode == "A":
                        
                        Matrice_APP[i][j] = "."
                        
                        # On décrémente le compteur
                        if Pointeur["bloc"] in Compteur:
                            Compteur[Pointeur["bloc"]] -= 1
                            
                # On affiche
                affiche_case(i, j, Matrice_APP[i][j], decalage)
        
        mise_a_jour()
def renvoiClic():
    '''
    Fonction qui renvoir le clic du joueur
    '''
    ev = donne_evenement()
    type_ev = type_evenement(ev)
    if "Clic" in type_ev:
        return (clic_x(ev), clic_y(ev), type_ev)
    mise_a_jour()
    
def attrCase(m,p):
    '''
    Attribue une position dans la matrice, un mode, et un clic en fonction du clic du joueur
    
    Si le joueur ne clique pas ou clique en dehors de la matrice (ex: quand la matrice est trop petite)
    on renvoie des -1, qui n'influence pas le return
    '''
    coords = renvoiClic()
    
    # Si pas de clic
    if coords is None:
        return -1,-1,-1,-1
    
    x, y, clic = coords[0] // 60, coords[1] // 60, coords[2]
    
    # Si clic dans le menu d'édition
    if y < 2:
        return x,y,"E",clic
        
    return x,y,"A",clic
    
    # Si clique pas dans la matrice
    return -1,-1,-1,-1
