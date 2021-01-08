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

### Caractéristiques

Chaque personnage possédé 6 attributs qui varient entre 30 et 90. Il s'agit des valeurs qui sont prises par effectuer un lancer de dé.

- STR (strength) : On utilisera cette valeur pour attaquer avec une arme du type `sword` ou pour toute action demandant de la force (ex: briser une porte)

- DEX (dexterity) : Utiliser pour attaquer avec un `arc` ou crocheter une porte.
  Aussi utiliser pour un lancer d'inactivité dans un combats (cela permet de determiné dans quels ordre les joueur et enemies doivent combattre)

- CON (constitution) : Quand on boit un potion de vie, on fait un lancer de `CON` pour determiner si le joueur à le droit à un bonus de vie. On peut aussi faire un test juste avant de mourir pour échapper à la mort (c'est la dernier chance). Ce nombre se limite en génerale à 1 mais peut varier en fonction de la difficulté.

- INT (Intelligence) : Un bonus s'applique sur les sorts en cas de réussite du lancer de dé.

- WIS (lucky) : Dans un coffre ou sur un ennemie , il y a deux types de loot . Le premier, loot ordinaire se trouvant dans la base de donné. Et le second qui est un loot qui apparaît seulement si le test est réussi, donc un meilleur loot.

- CHA (charisme) : A la rencontre d'un NPC , on effectue ce test pour determiner si le personnage joué arrive à charmer le NPC et pouvoir avoir des réduction sur le shop si c'est un marchand ou avoir des indications (direction/clef/porte) si cela est un NPC classic

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

En effet, il est possible de sauvegarder une partie en cours. Cependant, il n'y a pas de raccourcies claviers pour faire cela. En effet, il vous faudra trouver un feu de camps et de vous en approcher suffisamment pour que un appuie sur **espace** permettent de sauvegarder la partie.

![un feu de camps](/camp-fire.jpg)

Un message dans la console du jeu vous en avertira. Dès lors, quittez votre partie dans souci et revenez jouer plus tard.

Aussi, le feu de camps permet au joueur qui l'actionne de regagner tous ses points de vie.

## Camera

Nul besoin d'essayer de déplacer la caméra, vous ne pourrez pas le faire manuellement. En effet, elle vous suit automatique lorsque vous vous déplacer. Cependant, en appuyant sur **v**, vous pourrez alterner entre tous les heros présents sur la carte afin de changer la vision active. Pour changer le héro actif en temps réel, il suffit d'appuyer sur **c**

## Carte et minimap

Lors de vos parties, vous avez accès à une minimap. En début de partie, cette dernière va être toute noir. En effet, un brouillard de guerre est appliqué sur l'ensemble de la carte. Afin de voir la carte, il faut se déplacer dans le jeu et cela va automatique révéler la carte. Cependant, un léger brouillard va subsister. On peut voir sur la carte les points vers qui représente l'ensemble des joueurs et les points noirs qui sont l'ensemble des enemies.

Il est possible de voir la carte en grand en appuyant sur **u**. Cela va afficher sur la carte du jeu en grand. Dans le mode histoire, il est possible de voir les cartes des précedents niveaux et des niveaux suivants mais avec le brouillard de guerre qui bouche totalement la vue. Aussi, il est possible de dessiner sur les cartes en utilisant le crayon et d'effacer en utiliser la gomme. Pour passer de l'un à l'autre, il faut respectivement utiliser **r** et **e**. Il est aussi possible de réinitialiser le canvas de dessin avec **\*n** et évidemment, il est possible de le sauvegarder avec **ctrl+s**. C'est une fonction très pratique pour établir une stratégie d'attaque du donjons.

Il est aussi possible de créer ses propres cartes ! Pour cela, [vous trouverez des explications ici](/guides/dev/map).
