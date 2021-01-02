# Player

Chaque personnage posséde 6 attribut qui varie entre 30 et 90. Ceux sont les valeur qui seront prisent par effectuer un lancer de dé grace à la fonction `ThrowOfDice()`

```py
 def throwDice(self, Val, modificateur=0, valueOfDice=100):
        """Throw of dice like D&D

        Args:
            Val (int): [characteristic use for test like STR or INT]
            modificateur (int): [malus or bonus on your characteristic].
            Defaults to 0.
            valueOfDice (int): [value of dice]. Defaults to 100.

        Returns:
            [Boolean]: [Your reussit of test]
        """
        score = randint(0, valueOfDice)
        logger.info("Your dice is %i / 100 and the succes is under %i", score, Val+modificateur)
        return score <= Val + modificateur
```

## STR (strenght)

On utilisera cette valeur pour attaquer avec une arme du type `sword` ou pour toute action demandant de la force (ex: briser une porte)

## DEX (dexterity)

Utiliser pour attaquer avec un `arc` ou crocheter une porte.
Aussi utiliser pour un lancer d'iniativité dans un combats (cela permet de determiné dans quels ordre les joueur et enemie doivent combattre)

## CON (constitution)

Quand on boit un potion de vie, on fait un lancer de `CON` pour determiner si le joueur à le droit à un bonus de vie.

On peut aussi faire un test juste avant de mourir pour echapper a la mort(c'est la dernier chance). Ce nombre se limite en génerale à 1 mais peut varier en fonction de la difficulté.

## INT (Intelligence)

Un bonus s'applique sur les sorts en cas de réussite du lancer de dé.

## WIS (lucky)

Dans un coffre ou sur un enemie , il y a deux types de loot . Le premier, loot ordinaire se trouvant dans la base de donné. Et le second qui est un loot qui apparaît seulent si le test est réussi, donc un meilleur loot.

## CHA (charisme)

A la rencontre d'un NPC , on effectue ce test pour determiner si le personnage joué arrive à charmer le NPC et pouvoir avoir des réduction sur le shop si c'est un marchand ou avoir des indications (direction/clef/porte) si cela est un NPC classic
