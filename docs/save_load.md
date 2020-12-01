# Gestion de la progression

> Pour ne pas jouer des heures et des heures sans s'arrêter !

## Chargement

Lors du démarrage du jeu, si une précédente sauvegarde est trouvée alors elle est chargée dans le jeu. Pour ce faire, un écran de chargement apparaît lors du démariage du jeu. Au contraire, si rien n'est trouvé, alors le jeu va se lancer avec une nouvelle partie.

L'ensemble des parties sont stockées dans `assets/saved_games/`. Le fichier de création d'une nouvelle partie est stocké dans `data/game_data.py`. Il s'agit d'un grand dictionnaire qui contient toutes les données que l'utilisateur va être en mesure de sauvegarder.

La mécanique chargement est géré par l'écran `load_game` qui se charge avant le reste. Il permet de charger de la data et de l'injecter dans le state global

## Sauvegarde

Pour sauvegarder, l'utilisateur doit utiliser **CTRL+S**. Cela va stocker dans le dossier des sauvegardes une sauvegarde de l'état du jeu de l'utilisateur dans un fichier `json`.

La mécanique de sauvegarde est directement géré dans le fichier `window.py`.

## Gestion des données in-game

Il existe une variable qui transite d'écran en écran. Il s'agit de la variable `game_data`. Cette dernière permet donc d'y stocker tout un tas d'éléments que l'on souhaite conserver. En effet, il s'agit aussi de la variable qui est sauvegardée lors d'un **CTRL+s**.

On va retrouver 3 éléments dans cette dernière, qui se présente sous la forme d'un dictionnaire :

- les shortcuts, sous `shortcuts`
- les données du jeu, celles qui sont sauvegardées, sous `game_data`
- le nom du fichier de sauvegarde, sous `file_name`

::: warning

Les shortcuts sont sauvegardés dans leur propre fichier lors d'un ALT+s dans l'écran de visualisation et personnalisation des shortcuts.
Ainsi, uniquement les données du jeu sont sauvegardés lors d'un CTRL+s.

:::

### Donnés du jeu

Le fichier `data/game_data.py` est le fichier de base pour la sauvegarde. Il s'agit d'un template, chargée lors de la création d'une nouvelle partie, qui sera chargé dans `game_data["game_data"]`. Ainsi, il permet de visualiser la structure de nos données et non les données in-game, qui sont stockées dans `assets/saved_games`, chargée lors du chargement d'une partie. Ainsi, pour tout ajout dans la structure de données depuis l'un des écrans, cela doit d'abord se faire dans le fichier `game_data.py`.

Par exemple, dans l'écran de création d'un personnage, les caractéristiques du personnages sont enregistrées dans la variable `game_data` dans le champs `characteristics` comme nous le montre le template `data/game_data.py`.

```py
# on est dans game_data["game_data"]
"hero": { # on se place dans le dictionnaire lié à un personnage
    "class": "",
    "characteristics": { # on se place dans le dictionnaire lié aux caractéristiques d'un personnage
        "str": 0,
        "dex": 0,
        "con": 0,
        "int": 0,
        "wis": 0,
        "cha": 0
    }
}
```
