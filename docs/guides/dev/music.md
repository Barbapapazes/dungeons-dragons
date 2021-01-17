# Musique

Il est possible pour le joueur de régler la musique ainsi que sa présence dans les options du jeu. Il lui est aussi possible d'enregistrer ses préférences pour que cela soit conservé même lorsque l'utilisateur quitte la fenêtre.

Pour faire cette sauvegarder, lorsque le joueur appuie sur `ctrl + s` alors on va écrire un fichier json dans les `assets` dans le dossier `saved_music`. Lors du chargement du jeu, on va détecter si oui ou non il existe un fichier de paramètres. Si c'est le cas, alors on va le charger et le placer dans le game_data afin de le rendre disponible dans toutes les fenêtres.

Pour gérer la musique, on trouvera dans les managers, un musique manager qui s'occupe de jouer les sons, les charger...
