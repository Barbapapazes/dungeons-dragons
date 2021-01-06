# Jeu en ligne

Afin de pouvoir comment à jouer à plusieurs en ligne, il faut d'abord mettre en place le serveur. Pour cela, commencer par créer un fichier `.env` à la racine du projet. Ensuite copier et coller le contenu de `.local.env` dand le fichier nouvellement créer puis entrer vos informations.

## Démarrer le serveur

Vous devez au préalable avoir installé `pipenv`.

```sh
# lancer le serveur
$ pipenv run server
```

## Démarrer les clients

Il suffit de lancer l'application en utilisant `pipenv` puis de rentrer dans le mode de jeu en ligne. Vous pouvez lancer autant de client que vous le souhaitez.

## Erreurs

Il se peut que le serveur démarre après les clients même en lançant ces derniers après. Pour résoudre celà, il est conseillé d'utiliser le même terminal pour lancer serveur et client.
