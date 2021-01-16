# Raccourcis claviers

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

## Utilisation

Afin de pouvoir utiliser dans les customs shortcuts durant la création, il est possible d'utiliser la fonction `key_for` présente dans `utils/shortcuts`. C'est une fonction qui prend en paramètre la clé et un évènement. Avec ces 2 éléments, elle est en mesure de savoir si l'évènement correspond à la clé proposée. La clé qui lui est passé en paramètre provient du dictionnaire de clé au préalablement chargé, soit le default soit le fichier modifié par l'utilisateur au travers du menu shortcuts dans les options.
