# Fonctionnement global

> Les explications se rapportent principalement au fichier`./window.py` !

## Core

The core of the project is inside the file `main.py` and the file `window.py` under the class `Window`.

First of all, the main function is `main` under `Window`. This function is a loop where the state is run and the screen is updated.

These functions are able to manage screens !

Finalement, les 3 fonctions essentiels dans le fichier `window.py` sont

- **flip_state**, permet de réaliser le changement entre les écrans
- **events**, permet de gérer les events globaux et de transmettre au écran les évents
- **run**, permet de faire tourner les fonctions principales de chaque écran.

## Architecture générale

Le projet utilise des vues. Il s'agit de l'ensemble des fichiers qui se trouvent dans le dossiers `screens`. L'intégralité des fichiers sont des enfants des classes `_State` ou `_Elements` qui se trouve dans le fichier `window`. Ensuite les autres fonctionnalités sont répartis dans d'autres dossiers.

Dans le dossier `assets`, on va trouver l'ensemble des images pour le jeu mais aussi l'ensemble des fichiers de sauvegarde.

Dans le dossier `components`, on va trouver des composants comme un slider ou le menu déroulant.

Dans le dossier `config`, on va trouver un ensemble de fichiers dont le nom correspond à son contexte d'utilisation qui permet de réaliser des réglages et d'avoir un endroit pour les variables globales.

Dans le dossier `data`, on va trouver les fichiers de bases qui vont servir de base pour la création de data dans le jeu qui sera enregistrée ensuite dans les assets.

Dans le dossier `docs`, on va trouver l'ensemble de la documentation que vous être en train de lire.

Dans le dossier `inventory`, on va trouver tout ce qui se rapporte à l'inventaire et à la gestion des items.

Dans le dossier `manager`, on va trouver l'ensemble des managers du jeu tel que le versus, le tour par tout ou le logger en console in-game.

Dans le dossier `map` editor, on va trouver l'intégralité du map editor.

Dans le dossier `screens`, on va trouver l'ensemble des écrans du jeu.

Dans le dossier `server`, on va un fichier qui permet de gérer les clients (`network.py`) et un fichier qui permet de gérer les connexions au serveur (`main.py`).

Dans le dossier `sprites`, on va trouver l'ensemble des fichiers des sprites qui se trouve dans le jeu.

Dans le dossier `store`, on va trouver le store et le shop, un enfant du store.

Dans le dossier `utils`, il s'agit de fichier qui contiennent des fonctions ou des classes d'utilitaires.

## States

In the `main.py` file, all the states, which are called screens in this project, are loaded, using the `setup_states` function. They are classes which inherit from `_State` or from `_Elements`.

In the `Window`, there is a function called `flip_state` which is called every time the screen change. The goal is to load the new state and keep some data from the previous state. Ainsi, il est possible de transmettre de la data entre les différents écrans afin que ces derniers communiquent entre eux.

### Operation of a state

The `run` function from the `Window` class run the `run` function from the state. This function call a function depending of the chosen sub-state. For example, the `normal_run` is the main loop of a classique pygame project, which is often call `main`. Inside, we can call the `update`, `events` and `draw` functions. The call of this is to have the same design that for a single screen game. Multiple screens is now easy !

### Sub-states

Chaque écran peut avoir des sous états. C'est une fonction pratique qui permet de créer des sous menu sans avoir à changer d'écran. C'est donc beaucoup plus léger. Ainsi, la fonction `run` de l'écran choisir le bon sous état à faire tourner. Pour cela, on dispose d'un dictionnaire des sous états qui est fourni par la fonction `make_states_dict`. Ensuite, on appelant la fonction `toggle_sub_state` avec le nom du sous état voulu, nom qui est la clé du dictionnaire d'état, on peut changer de sous état.

If _done_ is set to true, the `flip_state` function, from the `Window` class, will load a new state, startup and the `global run` loop will run the `state run` loop, which run the sub-state function each frame !

### Différences entre \_State et \_Elements

La classe `_State` est la classe minimal pour créer un écran. En effet, on y trouve les fonctions `startup` ,`run`, `make_states_dict`,`normal_run`. Les fonctions sur les transitions vont permettre de générer de manière simplifier les transitions entres les écrans. C'est une classe qui comporte aussi des fonctions utilitaires comme `draw_text`, `load_data`.

La classe `_Elements` est un enfant de la classe `_State`. Ainsi, on profite de l'ensemble des éléments précédant mais avec des améliorations pour la gestion de l'interface. En effet, on va pouvoir charger très facilement un fond pour l'arrière. Aussi, la création des boutons, du bouton retour, l'affichage d'un titre, d'un sous-titre est aussi simplifiées.

Au final, `_Element` est très pratique pour la création d'un sous-menu.

## Screens

Les écrans sont gérés dans le dossier `screens` et ils représentent une vue de l'application.

Par exemple, on a l'écran de chargement du jeu, celui pour les crédits et même celui pour le jeu. Chacun d'eux est autonome et permet de gérer facilement et efficacement le développement de chacun des vue. En effet, la parallélisation des tâches est extrêmement simple, d'autant plus que la structure est classique avec pygame. Le seul ajout est celui des sub-state pour rester dans le même écran mais en y ajoutant des fonctionnalités.
