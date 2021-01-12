# Logger

Pour ce projet, nous avons rapidement mis en place le logger « logging », module natif de python afin de nous aider à développer. En effet, le logger permet de glisser dans son code des informations à stocker dans un fichier ou à imprimer dans la console. Un tel module permet de formater les messages en ajoutant de la couleur selon le niveau de criticités, l’heure d’enregistrement… Toutes ses informations permettent lors d’un bogue de savoir ce qui s’est passé en amont. C’est, si c’est bien implémenté, des informations qui permettent de corriger et de comprendre les bogues rapidement et qui évite d’utiliser les « print ». Il permet de s’assurer du bon fonctionnement du programme en récoltant les bonnes données.

Il est possible de changer le niveau de log en utilisant un `.env` à la racine du projet et en écrivant dedans :

```sh
PYTHON_ENV=production
```

Ainsi, le log level passera en Error qui permet d'éviter tous les logs d'informations.
