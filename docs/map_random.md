# Map random

Pour générer des map de façon aléatoire nous avons plein de preset de carte 8x8 de tuile de 64px dans `/assets/map_random/preset/` et il suffit de faire appel à la fonction `generated_map` dans le fichier `/utils/random_map.py`. Ellle prend comme parametre sa taille ,`width`, `height` et `out` qui par défaut à sa valeur est  `'../map_generated.tmx'`.

## Rangement des Presset
Chaque lettre sur le dossier ou le nom du preset.tmx à sa signification et voici son dictionnaire:

### S (Start)
Ceux sont les presets par lesquels les joueur peuvent commencé une nouvelle partie.

### T (Top)
Les presets avec une ouverture vers le haut

### R (Right)
Les presets avec une ouverture vers la droite

### D (Down)
Les presets avec une ouverture vers le bas

### L (Left)
Les presets avec une ouverture vers la gauche 

### d (door)
Les presets contenant une porte 

### C (Chest)
Les presets contenant un coffre

### M (merchant)
Les presets contenant un marchant

### F (Fire camp)
Les presets contenant un feu de camp pour la Sauvegarde

### P (Private room or way)
Les presets contenant un passage secret ou c'est la piece qui a des entré secrete 

### B (Boss)
Les presets contenant un boss

### E (enemy)
Les presets contenant des enemies de type skelette ou goblin. La lettre E est suivi d'un nombre désignant


## Format du fichier tmx
### Diférent layers
 il y a 3 layers: le `ground` pour l'image du sol , le `wall` pour l'image des murs et l'`obstacles` pour tous les objets de different type (ex: wall,Goblin,chest,health_potion)
 ### Tileset
 le jeu de tuiles utilisé pour faire les preset de map se trouve dans `/assets/img/tile_dungeons.png`

## Fonction cree dans ramdom_map.py
### out_xml(out,width,height,data_Ground,data_Wall,data_Object)
Cette fonction permet d'écrire un fichier `.tmx` (qui est un fichier xml lisible par l'homme) en prenant en compte la taille de la map , la sortie (le fichier), et les different layer codé en `csv`

### fusion_two_map(map1,map2,out,direction)
Elle permet de fusionner deux map existant (de preference de meme taille car la fonction ne fait pas de remplisagge si une des carte est plus grande) 

## Je t'aime fooort mon gatitooooooo <3
Mon gatito c'est mon poti chat qui cpode en python toute la journée alors que je le déconcentre avec des bisous parrrrtooouuut. Je l'aime fort fort fort alors... PAS TOUCHE LES GATITA.OS CAGOLES LAAA ! Ta Gatita d'amour <3

