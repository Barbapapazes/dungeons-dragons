# How this project works

## Core

The core of the project is inside the file `main.py` and the file `window.py` under the class `Window`.

First of all, the main function is `main` under `Window`. This function is a loop where the state is run and the screen is updated.

These functions are able to manage screens !

## States

In the `main.py` file, all the states, which are called screens in this project, are loaded, using the `setup_states` function. They are classes which inherit from `_State`.

In the `Window`, there is a function called `flip_state` which is called every time the screen change. The goal is to load the new state and keep some data from the previous state.

### Operation of a state

The `run` function from the `Window` class run the `run` function from the state. This function call a function depending of the chosen sub-state. For example, the `normal_run` is the main loop of a classique pygame project, which is often call `main`. Inside, we can call the `update`, `events` and `draw` functions. The call of this is to have the same design that for a single screen game. Multiple screens is now easy !

### Sub-states

Each state can have sub-states. This is useful to create sub-menu inside a screen or smooth transition between screens. Because of the function `run` which choose the correct run function, from the `state_dict`, each frame, you've just to change the state name to change the loop.

If _done_ is set to true, the `flip_state` function, from the `Window` class, will load a new state, startup and the `global run` loop will run the `state run` loop, which run the sub-state function each frame !

## Screens

Les écrans sont gérés dans le dossier `screens` et ils représentent une vue de l'application.

Par exemple, on a l'écran de chargement du jeu, celui pour les crédits et même celui pour le jeu. Chacun d'eux est autonome et permet de gérer facilement et efficacement le développement de chacun des vue. En effet, la parallélisation des tâches est extrêmement simple, d'autant plus que la structure est classique avec pygame. Le seul ajout est celui des sub-state pour rester dans le même écran mais en y ajoutant des fonctionnalités.
