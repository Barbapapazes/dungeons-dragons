# Déroulement d'un combat

> L'ensemble des configurations se trouve dans `config\versus.py`

## Initialisation

On considère que un personnage de class Voleur aura toujours l'initiative et commencera donc le combat. Pour ce qui concerne les autres entités personnage/ennemie, on effectue un jet sur l'attribut `DEX` (Dexterity). Ceux qui réussissent le mieux leur teste passe devant.

## Phase d'un joueur

Chaque joueur dispose d'un certain nombre d'action (définie par `numberOfAction`) . Ce dernier dispose de 2 action basic qui sont Attack et Move et s'il on est un Mage, on dispose d'une capacité en plus qui est Sort. Il est intéressant de noter que chaque action du joueur réduit de 1 son nombre d'action pour le tour.

### Attaquer

Tout abord s'il le joueur n'as pas d'arme , on considère qu'il tape à main nue et que ce dernier a une distance `TOUCH_HAND` de rayon et fait des dégâts de `DMG_ANY_WEAPON`.

S'il a une arme sélectionner, on peut distinguer part 2 type `sword` et `arc` :

Avec le type `sword`, un cercle se dessine autour du player définissant la porté de l'arme, puis nous devons sélectionner un ennemie . Si ce dernier ce trouve hors porté ,dommage une action est consommé. Mais si l'ennemie se trouve a porté, un lancer de `STR` est effectué pour determiné s'il l'attaque touche.

Avec le type `arc`, on considère que l'on peut tiré de n'importe où mais un malus proportionnel s'appliquer sur le lancer de `DEX`

```py
dist = self.distance(player, self.selectEnemy)
scope = player.weapon.scope
if scope < dist:
    malus = -((dist - scope) // TILESIZE) * MALUS_ARC
```

### Se déplacer

Créer un cercle de rayon `DISTANCE_MOVE` puis on sélectionne une position dans le cercle. Le personnage se déplace automatique grace à la fonction de pathfinding.

### Lancer un sort

Chaque utilisation de sort a un coût en mana , et chaque sort pose au sol une zone d'effet qui rend des point de vie pour les sort de type `heal` et les autres des dégât.

Un même sort peut appliquer des zones qui ont une valeur d'action différente (heal/dommage) car le sort fait comme les armes est possède une caractéristique xdz (x dé de valeur z)
