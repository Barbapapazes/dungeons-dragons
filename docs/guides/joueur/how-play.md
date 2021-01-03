# Comment jouer

> Présentation du mode de jeu en local

Après avoir créé une nouvelle partie, ou chargé une ancienne partie, il est venu le temps de joueur !

## Modes de jeu

Notre jeu a 2 modes de jeu, un temps réel, pour accélérer les phases de jeu hors combat, et un mode tour par tour pour les phases de combat.

Le tour par tour démarre automatiquement dès l'approche d'un enemy. Avant que ce dernier de démarre, un avertissement vous sera donné dans la console du jeu. Si vous approchez encore, alors le combat démarrera. A chaque tour, le personnage actif se voit remettre un certains nombre d'actions qu'il peut utiliser durant son tour.

## Déplacement

### Temps réel

En temps réel, le joueur peut se déplacer comme il le souhaite en utilisant les touches **ZQSD**. Attention aux murs et aux obstacles, le joueur ne peut pas les franchir.

### Tour par tour

En tour par tour, il vous faudra utiliser une action de mouvement afin de déplacer le hero librement dans un espace délimité par un cercle.

## Heros

Il existe 3 types de heros :

- le soldat
- le sorcier
- le voleur

Chacun de ses heros va se voir attribuer des capacités spéciales ainsi que des caractéristiques par défault différents.

### Soldat

Le soldat est un personnage sans capacité spécial. En revanche, il va être doté d'une grande force lui permettant de gagner ses combats et de mettre la misère à ses adversaires.

### Sorcier

Le sorcier est un personnage qui va pouvoir utiliser un sort lors de ses actions de tour par tour. Ces derniers vont permettre de redonner la vie ou d'en enlever aux personnages se trouvant à proximité de la zone d'effet du sort.

### Voleur

Le voleur est un personnage assez simple. Cependant, il a toujours la chance d'être le premier lorsque le tour par tour s'active.

## Enemies

## Items

### Au sol

Il existe différents types d'items à récupérer et utiliser.

- les morceaux d'armures
- les armes
- les potions
- les sorts
- les objets diverses (comme les clés)

Lorsque item est au sol il peut être récupéré par l'ensemble des personnages de la carte. Ainsi, un enemy peut récupéré des items. Cependant, lorsque ce dernier meurt, il relâche l'intégralité de son inventaire.

### Dans l'inventaire

Pour accéder à l'inventaire du joueur actif, il suffit de cliquer sur **ctrl+i**. Vous entrerez alors dans un sous écran vous permettant de gérer l'intégralité de votre stuff. Pour le gérer, vous pouvez utiliser le drag and drop ou bien vous laissez guider par un clique-droit sur l'item que vous souhaitez déplacer. Au center, vous allez pouvoir gérer l'équipement de votre héro, comme son arme de combat ou son armure.

## Sauvegarder le jeu

En effet, il est possible de sauvegarder une partie en cours. Cependant, il n'y a pas de raccourcies claviers pour faire cela. En effet, il vous faudra trouver un feu de camps et de vous en approcher suffisamment pour que un appuie sur **espace** permettent de sauvegarder la partie. Un message dans le

![un feu de camps](/camp-fire.jpg)

console du jeu vous en avertira. Dès lors, quittez votre partie dans souci et revenez jouer plus tard.

## Camera

Nul besoin d'essayer de déplacer la caméra, vous ne pourrez pas le faire manuellement. En effet, elle vous suit automatique lorsque vous vous déplacer. Cependant, en appuyant sur **v**, vous pourrez alterner entre tous les heros présents sur la carte afin de changer la vision active. Pour changer le héro actif en temps réel, il suffit d'appuyer sur **c**
