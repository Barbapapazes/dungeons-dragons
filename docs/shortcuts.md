# Raccourcis claviers

`il faut absolument revoir les shortcuts`
v : changer la vue camera
espace : interagir avec l'environnement

L'ensemble des shortcuts par défault sont dans `data/shortcuts.py`. Il s'agit d'un grand dictionnaire découpé en namespace en fonction des écrans. Ensuite, chaque shortcut est aussi un dictionnaire composé du raccourcie, sous la clé `keys`, et d'une phrase d'aide, sous la clé `help`.

Dans la clé `keys`, on va trouver une liste de 3 éléments. Le premier et le second sont des modifiers. Le premier est la touche CTRL, la seconde est la touche ALT et la dernière est la touche d'activation

Par exemple :

```py
{
"load_game":  {
    "up": {"keys": [True, False, pg.K_UP], "help": "Used to select a game"},
}
```

On peut ici comprendre que l'action `up` est dans le namespace (donc pour l'écran) `load_game`. L'aide nous permet de comprend à quoi cette action sert. Et enfin, `keys` est `CTRL+UP`

## Shortcuts par default

::: warning Le namespace 'window'

Le namespace window est global à l'ensemble des écrans. Ainsi, il ne faut pas réutiliser dans des écrans les shortcuts qui y sont utilisés.

:::

### Window

| Nom  | Raccourci | Aide                             |
| :--: | :-------: | -------------------------------- |
| save |  ctrl+s   | Permet de sauvegarder une partie |
| fps  |     =     | Toggle le conteur de fps         |

### Load Game

|   Nom    | Raccourci | Aide                              |
| :------: | :-------: | --------------------------------- |
|    up    |    UP     | Permet de sélectionner une partie |
|   down   |   DOWN    | Permet de sélectionner une partie |
|  enter   |  RETURN   | Permet de charger une partie      |
| new game |   SPACE   | Permet de créer une partie        |

### Game

|    Nom    | Raccourci | Aide                |
| :-------: | :-------: | ------------------- |
| inventory |     i     | Toggle l'inventaire |
|   menu    |     m     | Toggle le sous menu |

### Player

|  Nom  | Raccourci | Aide                            |
| :---: | :-------: | ------------------------------- |
|  up   |     z     | Avancer                         |
| down  |     s     | reculer                         |
| left  |     q     | Tourne le joueur ver la gauche  |
| right |     d     | Tourne le joueur vers la droite |

### Shortcuts

|  Nom  | Raccourci | Aide                                  |
| :---: | :-------: | ------------------------------------- |
| show  |  ctrl+k   | Toggle le panneau de shortcuts        |
| reset |   alt+r   | Permet de réinitialiser les shortcuts |
| save  |   alt+s   | Sauvegarder les shortcuts             |

## Panneau de configuration des shortcuts
