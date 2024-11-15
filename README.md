Fonctionnalités

Écran d'accueil : Affiche les meilleurs scores et permet au joueur de commencer une nouvelle partie en appuyant sur "Entrée".
Mouvement du joueur : Le joueur se déplace en sautant (espace) pour éviter des ennemis et collecter des icônes.
Vitesse croissante : À mesure que le score augmente, la vitesse des ennemis et du fond augmente.
Gestion des collisions : Le jeu détecte les collisions entre le joueur et les ennemis ou les icônes.
Sauvegarde des scores : À la fin de chaque partie, le score, le numéro de la tentative et la durée sont sauvegardés dans un fichier CSV.
Écran de fin de jeu : Affiche le score et invite à saisir un nom, puis sauvegarde les données lorsque le joueur appuie sur "Entrée".
Commandes
Entrée : Commence une nouvelle partie ou valide un nom à la fin du jeu.
Espace : Le joueur saute.
Retour arrière : Supprime un caractère du nom du joueur (en mode saisie).
Sauvegarde des données

Les données des joueurs (nom, numéro de tentative, score et durée) sont sauvegardées dans un fichier CSV portant le nom du joueur. Le format du fichier est le suivant :

Attempt Number, Score, Duration (seconds)
1, 100, 30.5
2, 150, 40.2

Structure du Code

Initialisation de Pygame : Initialisation des ressources et des variables globales (taille de l'écran, images, sons, etc.).
Mécanisme de jeu : La boucle principale gère l'affichage, les entrées clavier, les collisions, et les déplacements.
Gestion des collisions : Le joueur doit éviter les ennemis tout en collectant les icônes pour marquer des points.
Sauvegarde : Les données du joueur sont enregistrées dans des fichiers CSV après chaque partie.
Fonctionnalités étendues : Bien que la communication avec Arduino via serial soit incluse, elle n'est pas utilisée dans cette version du jeu.

Axes d'amélioration : 
le controle du jeu par les boutons de l'arduino via serial ne fonctionne pas 
Si deux joueur s'alterne, le nombre de tentatives ne fonctionne plus (car remis à 0)
SI un joueur se trompe de pseudo un nouveau csv est créé et le nombre de tentatives est remis a 0 (comme précedemment)
