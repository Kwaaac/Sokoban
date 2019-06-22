Pour lancer le jeu ecrivez dans le terminal: python3 Sokoban.py


Extension:
	- Menu : 
Le menu est composé tout d'abord du menu principal. Ce menu principal est une image en arrière plan se qui nous facilite la tache. Dans ce menu principal, le joueur a le choix entre jouer , lire le didacticiel, crée son plateau et quitter le jeu.

le menu_map (fonction Menu_map() ): apres avoir séléctionné jouer, le menu affichera alors toute les maps disponibles qui sont dans le repertoire "Map". Ceci sont afficher 12 par 12 en 3 colonne de 4 lignes. Ces maps sont encadrés.

Afin d'afficher les maps sur plusieurs pages, nous avons utilisé un slice que nous modifions en fonction de la page.
Le choix de la map, le changement de page et le retour au menu principal est gérer par la fonction "zone_clicable ()".
		
Les difficultés du menu map : Afin d'éviter de faire une armée de if , nous avons dû travaillé sur une suite arthmétique. Cela nous a aussi permis de facilité l'affichage des textes et leurs encadrages.

La suite utilisé est la suivante : pour le texte , Un+1=Un+300 avec U0 = 120 ( 120 est l espace entre le coté gauche de la fenetre et le premier texte). Pour touver la limite dans une boucle for, j'ai du utilisé 121+300*nombre de niveau.

Pour les rectangle et les zone clicable, nous avons utilié la même suite mais nous avons du aussi ajouté la hauteur et longueur de chaque niveau.

L'appelle recursive de la fonction "Menu_map()" nous à causée des ennuies. En effet, lorsque l'on changeai de page puis selectionné un niveau, le return de la fonction "zone_clicable()" est perdu et est même appellé plusieur fois à cause de la récursivité.
							
Pour régler ce problème, nous avons dû mettre le choix de la map dans une liste nommé "choix" car malgré la recusrsivité, une liste est mutable donc on ne perd pas la map choisis. De plus, nous avons imposé une condition sur cette liste pour éviter d'appeller plusieurs fois la zone cliquable
							
le didacticiel (fonction didacticiel () )  : après avoir séléctionné le didactitiel, une image apparais montrant comment jouer au jeu. 
Puis, il y a 2 zone cliquable. Le premier ("Editer") affiche comment éditer et le second ("jouer") affiche comment jouer. Une flèche de retour est disponible aussi afin de retourner sur le menu principal.

l'éditeur (voir l'extension "éditeur")
quitter : permet de quitter le jeu.

	-Mode Tirer:

Il y a une petite particularité avec le mode tirer. En effet, nous avons un compteur d'action, et utiliser le mode Tirer augmente ce compteur. Le mode tirer se désactive volontairement si on fait un autre déplacement que Tirer une caisse (la pousser le desactive par exemple), c'est dans un but bien précis, pour nous, le mode tirer apporte beaucoup trop de facilité, donc pour ajouter un léger gout de challenge, nous pensons au joueur qui va tenter de faire un record d'actionc sur une map, et pour ça, il faudra utiliser le mode tirer avec parcimonie et sans l'utiliser à tout vas. A noter que nous avions déjà fait une versions qui ne se désactive moins facilement (pousser ne le désactivait pas par exemple), il suffit de retirer quelques conditions.

	-Editeur:

L'editeur va permettre de créer une map de la taille de son choix, et de modifier le plateau vide avec des éléments d'édition.
Il y un tuto sur comment l'utiliser qui est intégré au jeu.
L'editeur n'a pas eu de mal à s'intégré, j'ai surtout rencontré une légère difficulté sur la prise de donnée qui à été longue à mettre en place. Sinon, l'edition en lui même à été très simple à intégré dans la mesure ou une fois les coordonnées du clic récupérer, il suffisait de faire attention à ce que voulais le joueur et d'appliquer des changements en fonction.


LES PROBLEMES RENCONTRE:
La collision entre les caisses et les targets. En effet lorsque nous utilisions qu'une seul matrice de jeu, nous avons du trouver une alternative, soit la matrice calque qui permet aux caisses de passer litéralement au dessus des targets et des clés et par conséquent, d'éviter d'avoir à s'occuper des cas isolé (Caisse sur une target, caisse sur une clef...).


ORGANISATION DU PROGRAMME:

Le jeu est organisé tout d'abord d'une initialisation:
	-Ouverture du menu (Description de ce dernier ci-dessus).
	-Avec la fonction cree_matrice_jeu: création tout d'abord de la Matrice_jeu qui est une matrice issue de la lecture d'un fichier (map)
	-création d'une fenetre dont la taille est adaptée à la Matrice_jeu
	-avec la fonction creer_calque_jeu, création d'un calque: le calque est une matrice_jeu contenant seulement les clés ainsi que les targets.

Après l'initialisation, une boucle while est créé et va gérer le jeu. Donc à chaque tour de boucle :

	-avec la fonction affiche jeu,on réaffiche le jeu (qui a subit une mise à jour tel que des déplacements)
	-avec la fonction check_calque, on verifie si toute les boites sont sur les targets et également si le joueur à pris des clés
	-La fonction event va prendre en compte la touche selectioné par le joueur et le programme va appliquer les mesures affiliés au touches.
	-Avec la direction renvoyer par l'evenement, on va deplacer le gardien grace a la fonction deplace_gardien.


LES CHOIX TECHNIQUES:

les calques: Les calques nous permettent d'éviter de gérer les collisions entre les caisse et les targets. Si nous avions laissé les targets et les caisses sur une même matrice, on aurait été obligé de gérer la colisions entre elles et cela aurait porté préjudice à la lisibilité de notre code. 
Nous avons donc opté pour une matrice calque, et dans ce cas on doit simplement ne pas la négliger lors de la sauvegarde. 

changement de liste en matrice: Lors de la 1er étape du projet, nous avons vaguement abordé la notion de matrice, donc nous avions commencer à crée le jeu seulement avec les liste (ce qui allourdissait énormément le jeu) 

La fonction "Principale" Evenement : Afin de reduire le programme au maximum aux fonctions, nous avons crée une fonction evenement qui traduit la touche entré par le joueur et qui réagit en fonction

Utilisation des dictionnaires global: Utiliser ses dictionnaires nous à éviter une chose, balader les variables dans toutes les fonctions et avoir des paramètre à rallonge. Pour un peu d'espace mémoire utiliser en plus, cela nous permet d'améliorer la lisibilité du codede manière considérable, en plus d'être plus simple à programmer puisqu'on n'a pas à s'embeter à vérifier quel variable passe dans quel fonctions et qu'es-ce qu'on doit renvoyer dans le cas contraire etc.

Module FonctionCommunes: Un module à été effectuer car plusieurs de nos programme utilisait les mêmes fonctions, donc nous avons simplement regrouper ses fonctions

Repartitions des taches :
	La phase 1 n'est pas mentionner car elle à été effectuer sous forme de liste et de tuple (comme le tp sur le snake) plutot que sous forme de matrice donc toute la phase 1 à été refaite lors de la phase 2.

Maxime :

Phase 2:
	-Transition liste --> Matrice (à refait toute la phase 1 à l'exception de le fonction evenement et debug)
	-Lecture d'un fichier, savegarde et chargement de la carte, gestion des clés et des portes

Phase 3:
	-Mode Tirer
	-Editeur

Eric:


Phase2:
	-Fonction debug et evenement.
	-Vérification,ajustement et optimisation du code
Phase3:
	-Menu
