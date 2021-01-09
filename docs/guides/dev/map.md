# Map

Nos maps utilisent des fichiers standards `tmx`. Ce format de fichier permet une lecture aisé des cartes, un ajout important de méta-data et une création facilité des cartes.

## Les fichiers

### Création

Pour ce projet, nous avons mis en place un map éditor très simple mais tout de même très fonctionnel. Cependant, nous ne sommes pas allé dans les détails de l'outils car nous utilisons [Tiled](https://www.mapeditor.org/) pour créer nos cartes. Tiled est un utilitaire, facile d'utilisation qui permet de créer rapidement des cartes au format tmx à partir de tilesheets. Ainsi, c'est grâce à cet outil que nous avons réalisé toutes nos maps.

### Méta-data

Les fichiers `tmx` sont des fichiers `xml` avec une architecture spécifique pour les cartes. L'intérêt de ce type de fichiers, à l'inverse d'un fichier text, est qu'il permet de stocker et d'organiser très simplement nos données. Ainsi, avec ce type de fichiers, nous avons accès à plusieurs layers sur une carte et nous pouvons y ajouter un système d'objet directement dans la carte. Ce système d'objet permet à nos cartes une grandes flexibilités et une manipulation très simple. Lors de la lecture de cette dernière par le jeu, nous pouvons instancier le bon élément en utilisant le nom et la position de l'objet. C'est donc très pratique.

Le meilleur exemple est la gestion des items.

#### Gestion des items sur la carte

Afin de créer un item sur la carte, il suffit de créer un objet, dans un tag objectgroup, dont le nom est la clé du dictionnaire de l'élément voulu dans `sprites.py`.

Ainsi, en ajoutant :

```xml
<object id="1" name="bronze_key_small" x="336" y="400" width="32" height="32"/>
```

On va pouvoir créer une clé en bronze à la position 336, 400 sur la carte. Cependant, comme conseillé dans le guide du joueur, il est conseillé d'utiliser Tiled.

#### Gestion des télé-porteurs

Afin de pour réaliser une campagne, des niveaux qui se suivent, une continuité, il est possible de déposer sur la carte des télé-porteurs.

Afin de créer un télé-porteur in-game, il suffit de créer un objet avec un nom qui suit le pattern suivant:

`map-folder-filename`

:::info Conseil

Pour la création d'une campagne personnalisée avec vision des maps précédentes, il est conseillé d'utiliser `levels_maps` comme folder.

:::

Exemple :

```xml
<object id="1" name="map-saved_maps-level1.tmx" x="336" y="400" width="32" height="32"/>
```

Il est possible de trigger la fin du jeu avec `finish` à la place du filename.

#### Gestion des pièges

Afin de semer des embûches dans les parties, il est possible d'ajouter des pièges sur votre carte. Lorsque un caractère se déplace dessus, alors ce dernier va subir des dégâts et le piège s'activer.

Afin de générer un piège :

```xml
<object id="1" name="trap" x="336" y="400" width="32" height="32"/>
```

## Map editor

This map editor is used to create or edit a map for the game. It uses a GUI to facilitate the process of map creation. This tool is not inside the game which is different process. But we recommended to close the game when update a map for a better experience.

### Start the map editor

```sh
# start the map editor
$ pipenv run map_editor
```

### Shortcuts

- **CTRL + K**: show all shortcuts

#### In the tileset

- **Left Click**: select a tile
- **ZQSD or Scroll Wheel**: move the tileset

#### In the map

- **IJKL**: move the map in the viewport
- **Number**: select a layer
- **Left Click**: add a tile to the selected layer, drag to add many tiles
- **Right Click**: remove a tile from the selected layer, drag to remove many tiles
- **ALT + Left Click** (drag to draw): create a wall
- **ALT + Right Click** (inside a rect): remove a wall or a player
- **CTRL + R**: remove the selected tile
- **CTRL + S**: save the map

#### Tools

- **Paint Pot** (red square): select a layer, a tile and then click on the paint pot
- **Rubber** (yellow square): remove all tile from the selected layer
- **Player** (green square): create a player object

### About Tiled

Because our game support the standard `.tmx` files for saving map data, you can use [Tiled](https://www.mapeditor.org/) for a better experience.

## Map random

Pour générer des maps de façon aléatoire, il a été créé des presets de carte 8x8 avec des tuiles de 64px dans `/assets/map_random/preset/`. Ainsi, il suffit de faire appel à la fonction `generated_map` dans le fichier `/utils/random_map.py` pour générer une map. Elle prend comme paramètre sa taille ,`width`, `height` et `out` qui par défaut à sa valeur est `../map_generated.tmx`.

### Fonctions utiles

```py
def out_xml(out, width, height, data_Ground, data_Wall, data_Object):
  pass
```

Cette fonction permet d'écrire un fichier `.tmx` en prenant en compte la taille de la map , la sortie (le fichier), et les différentes layers codée en `csv`.

```py
def fusion_two_map(map1, map2, out, direction):
  pass
```

Elle permet de fusionner deux map existantes, de préférences de même taille car la fonction ne fait pas de remplissage si une des carte est plus grande.

### Rangement des presets

Chaque lettre sur le dossier ou le nom du preset.tmx à sa signification et voici son dictionnaire:

- S (Start) : Il s'agit des presets par lesquels les joueur peuvent commencer une nouvelle partie.

- T (Top) : Les presets avec une ouverture vers le haut.

- R (Right) : Les presets avec une ouverture vers la droite

- D (Down) : Les presets avec une ouverture vers le bas

- L (Left) : Les presets avec une ouverture vers la gauche

- d (door) : Les presets contenant une porte

- C (Chest) : Les presets contenant un coffre

- M (merchant) : Les presets contenant un marchant

- F (Fire camp) : Les presets contenant un feu de camp pour la Sauvegarde

- P (Private room or way) : Les presets contenant un passage secret ou c'est la piece qui a des entré secrete

- B (Boss) : Les presets contenant un boss

- E (enemy) : Les presets contenant des enemies de type squelette ou goblin. La lettre E est suivi d'un nombre désignant

### Fichier généré

#### Les layers

Il y a 3 layers :

- le `ground` pour l'image du sol
- le `wall` pour l'image des murs
- l'`obstacles` pour tous les objets de différents types (ex: wall,Goblin,chest,health_potion)

Le jeu de tuiles utilisé pour faire les presets de map se trouve dans `/assets/img/tile_dungeons.png`. C'est donc ce dernier qui va permettre de générer l'intégralité de la carte.
