# Démarrer le jeu

Avant même de commencer à joueur au jeu, il va falloir le démarrer. Pour cela, il vous faut à minima [python 3.9](https://python.org) installé sur votre machine avec `pip`.

Ensuite, il faut démarrer un terminal dans le path du projet puis lancer les commandes suivantes :

```sh
# install a local environment
$ pip install pipenv
# install all packages
$ pipenv install
# start the project
$ pipenv run start
```

Voilà ! Vous êtes fin prêt à commencer à découvrir le jeu ! Mais vous pouvez aussi continuer à lire le guide !

:::tip

### Env

As you can see, there is a `.env.local` file. To enable feature like production mode or online mode, you have to create a copy of it and call it `.env`.

For production:

```txt
PYTHON_ENV=production
```

For online game (only add this key to play online, otherwise, remove it):

```txt
SERVER_IP=178.79.177.210 (this IP is the remote server)
```

:::
