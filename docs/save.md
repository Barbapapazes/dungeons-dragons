# Gestion de la progression

> Pour ne pas jouer des heures et des heures sans s'arrêter !

::: warning
Pour le moment, une seule sauvegarde est possible ! Une mise à jour devrait bientôt permettre de gérer la multi sauvegarde.
:::

## Chargement

Lors du démarrage du jeu, si une précédente sauvegarde est trouvée alors elle est chargée dans le jeu. Pour ce faire, un écran de chargement apparaît lors du démariage du jeu. Au contraire, si rien n'est trouvé, alors le jeu va se lancer avec une nouvelle partie.

L'ensemble des parties sont stockées dans `assets/saved_games/`. Le fichier de création d'une nouvelle partie est stocké dans `data/game_data.py`. Il s'agit d'un grand dictionnaire qui contient toutes les données que l'utilisateur va être en mesure de sauvegarder.

La mécanique chargement est géré par l'écran `load_game` qui se charge avant le reste. Il permet de charger de la data et de l'injecter dans le state global

## Sauvegarde

Pour sauvegarder, l'utilisateur doit utiliser **CTRL+S**. Cela va stocker dans le dossier des sauvegardes une sauvegarde de l'état du jeu de l'utilisateur dans un fichier `json`.

La mécanique de sauvegarde est directement géré dans le fichier `window.py`.
