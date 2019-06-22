from upemtk import *
from os import listdir
from Editeur import *
from FonctionCommunes import *

#Module de menu pour le SOKOBAN/ utilitaire

def coordonne():
    """
    Renvoie les coordonne (x,y)
    """
    Coordonne=attente_clic()

    return Coordonne[0],Coordonne[1]


######################################## Fonction menu map
def Presenter_Map (niveau,y):
    """
    Fonction qui permet de presenter des niveau dans le menu map sur une ligne
    """
    indice=0
    Nblvl=len(niveau)-1

    #120= espacement entre le 1er texte et la droite de la fenetre / 300=espacement entre 2 texte / 121+300*Nblvl= Nblvl ajuste la taille maximum dela taille entre la partie droite de la fenetre et le dernier texte
    for x in range (120,121+300*Nblvl,300):
        texte(x,y,niveau[indice],couleur='white', police = "Dejavu")
        indice+=1

    mise_a_jour()
    
def zone_clicable(debut,fin,indic,ALL_Map,liste):
    """
    Fonction qui permet au programme de réagir en fonction du clic de l utilisateur (Changement de page et selection de noveau
    """

    #on prend les coordonnée x et y
    x,y=coordonne()

    ################ Selection de niveau ################

    #l'indice nous permettra de récuperer le niveau grâce à " ALL_Map[indice] "
    indice = debut
    h = hauteur_texte()

    # La suite et les valeurs suivante corresponde au rectangle qui entoure les textes
    for ya in range(200, 651, 150):
        for xa in range(120, 721, 300):

            #Si l indice est deja superieur à la longueur de ALL_Map, on arrete notre boucle et on arrete la verification / ( permet aussi d'annuler l'effet de la fonction dans les endroits ou il peut y avoir un niveau en fonction de ALL_Map)
            if indice>len(ALL_Map)-1:
                break

            #Verification si le x et y sont dans un recangle
            if xa - 10 < x < xa + 10 + longueur_texte(ALL_Map[indice]) and ya < y < ya + h:

                if len(liste) != 0:
                    liste[0] = ALL_Map[indice]
                
                else:
                    liste.append(ALL_Map[indice])
                return liste

            # On augmente l'indice
            indice += 1






    ####### CHANGEMENT DE PAGE ############

    #Fleche Basse /  Les valeurs de comparaison correspondent au pixel ou apparaissent les fleches / la variable indic nous permet d'annuler la zone clicable sur la fleche basse si il n'y a pas d'autre niveau à afficher
    if 925<x<970 and 680<y<730 and indic==True:

        #On ajuste le debut et la fin du slice pour afficher les niveaux d'après
        debut+=12
        fin+=13
        Menu_Map(debut,fin)
        pass

    #fleche haute / La condition debut!=0 nous pemet d'annuler l'action de la fleche haute si nous somme déja sur la 1er page
    elif 925<x<970 and 575<y<630 and debut!=0:

        #On ajuste le debut et la fin du slice pour afficher les niveau d'avant

        debut+=-12
        fin+=-13
        Menu_Map(debut,fin)
        pass
    
    
    elif 0<x<50 and 0<y<50 :
        menu()
        
    else:
        zone_clicable(debut,fin,indic,ALL_Map,liste)






def Menu_Map(debut=0,fin=12,liste=[], edition = False):
    """
    Fonction principal du menu map qui permet d'afficher le niveau et demande au joueur de cliquer
    """

    #Debut,Fin = Dans le cas ou une page ne suffit pas pour afficher les niveaux,on va utiliser un slice sur une liste contenant toute les maps (ALL_Map). Ces variable vont etre ajuster pour afficher d'autre niveau

    #Appelle de l'image d'arriere plan
    image(500, 375, "Image/Menu_Map.png")

    #Affichage du numero de page
    texte (935,630,fin//12,couleur="white", police = "Dejavu")



    #initialisation

    #on prend tt les map du repertoire Map
    ALL_Map=sorted(listdir("Map"))
    
    if edition == True:
        ALL_Map.insert(0, "Nouvelle Map")
    #Dans le cas ou il faut un menu deroulant, on affiche les fleche et prend seulement une partie des maps qui seront affiché
    if len(ALL_Map)>12 :
        map = ALL_Map[debut:fin]

        #affichage fleche basse
        if fin<=len(ALL_Map):
            image (950,700,"Image/Fleche_basse.gif")


        #affichage fleche haute
        if debut>0:
            image (950,600,"Image/Fleche_Haute.gif")


    #Dans le cas ou on a pas besoin de menu deroulent
    else:
        map=list(ALL_Map)



    ########
    #permettra de bloquer l action des menu deroulant (zone cliquable) si on a deja afficher tt les maps disponible
    if fin>len(ALL_Map):
        indic=False
    else:
        indic=True
    ############################

    #y=espace entre le haut de la fenetre et le 1er texte
    y=200
    while map!=[]:

        ranger_de_niveau=[]

        if len(map)>=3:

            #on divise la liste afin d obtenir 3 map
            for i in range (3):
                ranger_de_niveau.append(map.pop(0))

            #que l on affiche
            Presenter_Map(ranger_de_niveau,y)

            #et que l on encadre
            entourage (ranger_de_niveau,y)

            y+=150

            continue
        else:
            # on affiche le reste des map
            Presenter_Map(map, y)

            # on affiche le rectangle autour des maps
            entourage(map, y)

            # on vide maps pour sortir du while
            map = []


    ############################

    #afin d'éviter d'avoir plusieur fois la fonction zone_clicable, on va stocker le return dans une liste et la tester si il y a bseoin ou non de reappeller cette fonction.
    #De plus, a cause de la recursivité on peux perdre notre return de zone_clicable donc on le met dans une liste qui , lui , n est pas affecter par le récursiviter

    zone_clicable(debut, fin, indic, ALL_Map, liste)
    return liste[0]
    
        
def entourage(ranger_de_niveau,y):
    """
    Fonction qui permet d'encadrer les niveau
    """
    #on utilise ondice pour appeller les elm de ranger_de_niveau
    indice=0

    hauteur=hauteur_texte()

    #On prend la taille de la liste afin de pouvoir gerer les cas ou la liste est inferieur a 4
    Nblvl=len(ranger_de_niveau)-1

    #Valeur correspondant a mes suite
    for x in range (120,+121+300*Nblvl,300):
        rectangle(x-10,y,x+10+longueur_texte(ranger_de_niveau[indice]),y+hauteur,couleur="blue",epaisseur=5)
        indice+=1

    mise_a_jour()

################### Didacticiel#############
def didacticiel ():
    image (500,375,"Image/Didacticiel_Jeu.png")
    while True:
        x,y=coordonne()


        #Editer
        if 220<x<470 and 105<y<170:
            efface_tout()
            image(500, 375, "Image/Didacticiel_Jeu.png")

        #Jouer
        elif 515<x<725 and 105<y<170:
            efface_tout()
            image(500, 375, "Image/Didacticiel_Editeur.png")

        # retour menu
        elif 0<x<50 and 0<y<50 :
            break
    pass


def menu():
    """
    Fonction qui permet au menu de réagir en fonction des endroit clique
    """
    
    a=0
    
    while a == 0 :
        image(500,375,"Image/Menu_sokoban1.png")
        x,y=coordonne()


        #Jeu
        if 414<x<597 and 200<y<258:
            a=1
            return Menu_Map()

        #Didactielle
        if 344<x<663 and 340<y<403:
            efface_tout()
            didacticiel()


        #Editer
        if 419<x<590 and 483<y<542:
            efface_tout()
            
            demandeTaille()
            
            ferme_fenetre()
            cree_fenetre(1000,750)
        
        
        #fermeture de la fenetre
        if 402<x<611 and 623<y<683:
            exit()
