(window.webpackJsonp=window.webpackJsonp||[]).push([[17],{374:function(e,s,t){"use strict";t.r(s);var n=t(25),a=Object(n.a)({},(function(){var e=this,s=e.$createElement,t=e._self._c||s;return t("ContentSlotsDistributor",{attrs:{"slot-key":e.$parent.slotKey}},[t("h1",{attrs:{id:"fonctionnement-global"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#fonctionnement-global"}},[e._v("#")]),e._v(" Fonctionnement global")]),e._v(" "),t("blockquote",[t("p",[e._v("Les explications se rapportent principalement au fichier"),t("code",[e._v("./window.py")]),e._v(" !")])]),e._v(" "),t("h2",{attrs:{id:"core"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#core"}},[e._v("#")]),e._v(" Core")]),e._v(" "),t("p",[e._v("The core of the project is inside the file "),t("code",[e._v("main.py")]),e._v(" and the file "),t("code",[e._v("window.py")]),e._v(" under the class "),t("code",[e._v("Window")]),e._v(".")]),e._v(" "),t("p",[e._v("First of all, the main function is "),t("code",[e._v("main")]),e._v(" under "),t("code",[e._v("Window")]),e._v(". This function is a loop where the state is run and the screen is updated.")]),e._v(" "),t("p",[e._v("These functions are able to manage screens !")]),e._v(" "),t("p",[e._v("Finalement, les 3 fonctions essentiels dans le fichier "),t("code",[e._v("window.py")]),e._v(" sont")]),e._v(" "),t("ul",[t("li",[t("strong",[e._v("flip_state")]),e._v(", permet de réaliser le changement entre les écrans")]),e._v(" "),t("li",[t("strong",[e._v("events")]),e._v(", permet de gérer les events globaux et de transmettre au écran les évents")]),e._v(" "),t("li",[t("strong",[e._v("run")]),e._v(", permet de faire tourner les fonctions principales de chaque écran.")])]),e._v(" "),t("h2",{attrs:{id:"architecture-generale"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#architecture-generale"}},[e._v("#")]),e._v(" Architecture générale")]),e._v(" "),t("p",[e._v("Le projet utilise des vues. Il s'agit de l'ensemble des fichiers qui se trouvent dans le dossiers "),t("code",[e._v("screens")]),e._v(". L'intégralité des fichiers sont des enfants des classes "),t("code",[e._v("_State")]),e._v(" ou "),t("code",[e._v("_Elements")]),e._v(" qui se trouve dans le fichier "),t("code",[e._v("window")]),e._v(". Ensuite les autres fonctionnalités sont répartis dans d'autres dossiers.")]),e._v(" "),t("p",[e._v("Dans le dossier "),t("code",[e._v("assets")]),e._v(", on va trouver l'ensemble des images pour le jeu mais aussi l'ensemble des fichiers de sauvegarde.")]),e._v(" "),t("p",[e._v("Dans le dossier "),t("code",[e._v("components")]),e._v(", on va trouver des composants comme un slider ou le menu déroulant.")]),e._v(" "),t("p",[e._v("Dans le dossier "),t("code",[e._v("config")]),e._v(", on va trouver un ensemble de fichiers dont le nom correspond à son contexte d'utilisation qui permet de réaliser des réglages et d'avoir un endroit pour les variables globales.")]),e._v(" "),t("p",[e._v("Dans le dossier "),t("code",[e._v("data")]),e._v(", on va trouver les fichiers de bases qui vont servir de base pour la création de data dans le jeu qui sera enregistrée ensuite dans les assets.")]),e._v(" "),t("p",[e._v("Dans le dossier "),t("code",[e._v("docs")]),e._v(", on va trouver l'ensemble de la documentation que vous être en train de lire.")]),e._v(" "),t("p",[e._v("Dans le dossier "),t("code",[e._v("inventory")]),e._v(", on va trouver tout ce qui se rapporte à l'inventaire et à la gestion des items.")]),e._v(" "),t("p",[e._v("Dans le dossier "),t("code",[e._v("manager")]),e._v(", on va trouver l'ensemble des managers du jeu tel que le versus, le tour par tout ou le logger en console in-game.")]),e._v(" "),t("p",[e._v("Dans le dossier "),t("code",[e._v("map")]),e._v(" editor, on va trouver l'intégralité du map editor.")]),e._v(" "),t("p",[e._v("Dans le dossier "),t("code",[e._v("screens")]),e._v(", on va trouver l'ensemble des écrans du jeu.")]),e._v(" "),t("p",[e._v("Dans le dossier "),t("code",[e._v("server")]),e._v(", on va un fichier qui permet de gérer les clients ("),t("code",[e._v("network.py")]),e._v(") et un fichier qui permet de gérer les connexions au serveur ("),t("code",[e._v("main.py")]),e._v(").")]),e._v(" "),t("p",[e._v("Dans le dossier "),t("code",[e._v("sprites")]),e._v(", on va trouver l'ensemble des fichiers des sprites qui se trouve dans le jeu.")]),e._v(" "),t("p",[e._v("Dans le dossier "),t("code",[e._v("store")]),e._v(", on va trouver le store et le shop, un enfant du store.")]),e._v(" "),t("p",[e._v("Dans le dossier "),t("code",[e._v("utils")]),e._v(", il s'agit de fichier qui contiennent des fonctions ou des classes d'utilitaires.")]),e._v(" "),t("h2",{attrs:{id:"states"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#states"}},[e._v("#")]),e._v(" States")]),e._v(" "),t("p",[e._v("In the "),t("code",[e._v("main.py")]),e._v(" file, all the states, which are called screens in this project, are loaded, using the "),t("code",[e._v("setup_states")]),e._v(" function. They are classes which inherit from "),t("code",[e._v("_State")]),e._v(" or from "),t("code",[e._v("_Elements")]),e._v(".")]),e._v(" "),t("p",[e._v("In the "),t("code",[e._v("Window")]),e._v(", there is a function called "),t("code",[e._v("flip_state")]),e._v(" which is called every time the screen change. The goal is to load the new state and keep some data from the previous state. Ainsi, il est possible de transmettre de la data entre les différents écrans afin que ces derniers communiquent entre eux.")]),e._v(" "),t("h3",{attrs:{id:"operation-of-a-state"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#operation-of-a-state"}},[e._v("#")]),e._v(" Operation of a state")]),e._v(" "),t("p",[e._v("The "),t("code",[e._v("run")]),e._v(" function from the "),t("code",[e._v("Window")]),e._v(" class run the "),t("code",[e._v("run")]),e._v(" function from the state. This function call a function depending of the chosen sub-state. For example, the "),t("code",[e._v("normal_run")]),e._v(" is the main loop of a classique pygame project, which is often call "),t("code",[e._v("main")]),e._v(". Inside, we can call the "),t("code",[e._v("update")]),e._v(", "),t("code",[e._v("events")]),e._v(" and "),t("code",[e._v("draw")]),e._v(" functions. The call of this is to have the same design that for a single screen game. Multiple screens is now easy !")]),e._v(" "),t("h3",{attrs:{id:"sub-states"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#sub-states"}},[e._v("#")]),e._v(" Sub-states")]),e._v(" "),t("p",[e._v("Chaque écran peut avoir des sous états. C'est une fonction pratique qui permet de créer des sous menu sans avoir à changer d'écran. C'est donc beaucoup plus léger. Ainsi, la fonction "),t("code",[e._v("run")]),e._v(" de l'écran choisir le bon sous état à faire tourner. Pour cela, on dispose d'un dictionnaire des sous états qui est fourni par la fonction "),t("code",[e._v("make_states_dict")]),e._v(". Ensuite, on appelant la fonction "),t("code",[e._v("toggle_sub_state")]),e._v(" avec le nom du sous état voulu, nom qui est la clé du dictionnaire d'état, on peut changer de sous état.")]),e._v(" "),t("p",[e._v("If "),t("em",[e._v("done")]),e._v(" is set to true, the "),t("code",[e._v("flip_state")]),e._v(" function, from the "),t("code",[e._v("Window")]),e._v(" class, will load a new state, startup and the "),t("code",[e._v("global run")]),e._v(" loop will run the "),t("code",[e._v("state run")]),e._v(" loop, which run the sub-state function each frame !")]),e._v(" "),t("h3",{attrs:{id:"differences-entre-state-et-elements"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#differences-entre-state-et-elements"}},[e._v("#")]),e._v(" Différences entre _State et _Elements")]),e._v(" "),t("p",[e._v("La classe "),t("code",[e._v("_State")]),e._v(" est la classe minimal pour créer un écran. En effet, on y trouve les fonctions "),t("code",[e._v("startup")]),e._v(" ,"),t("code",[e._v("run")]),e._v(", "),t("code",[e._v("make_states_dict")]),e._v(","),t("code",[e._v("normal_run")]),e._v(". Les fonctions sur les transitions vont permettre de générer de manière simplifier les transitions entres les écrans. C'est une classe qui comporte aussi des fonctions utilitaires comme "),t("code",[e._v("draw_text")]),e._v(", "),t("code",[e._v("load_data")]),e._v(".")]),e._v(" "),t("p",[e._v("La classe "),t("code",[e._v("_Elements")]),e._v(" est un enfant de la classe "),t("code",[e._v("_State")]),e._v(". Ainsi, on profite de l'ensemble des éléments précédant mais avec des améliorations pour la gestion de l'interface. En effet, on va pouvoir charger très facilement un fond pour l'arrière. Aussi, la création des boutons, du bouton retour, l'affichage d'un titre, d'un sous-titre est aussi simplifiées.")]),e._v(" "),t("p",[e._v("Au final, "),t("code",[e._v("_Element")]),e._v(" est très pratique pour la création d'un sous-menu.")]),e._v(" "),t("h2",{attrs:{id:"screens"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#screens"}},[e._v("#")]),e._v(" Screens")]),e._v(" "),t("p",[e._v("Les écrans sont gérés dans le dossier "),t("code",[e._v("screens")]),e._v(" et ils représentent une vue de l'application.")]),e._v(" "),t("p",[e._v("Par exemple, on a l'écran de chargement du jeu, celui pour les crédits et même celui pour le jeu. Chacun d'eux est autonome et permet de gérer facilement et efficacement le développement de chacun des vue. En effet, la parallélisation des tâches est extrêmement simple, d'autant plus que la structure est classique avec pygame. Le seul ajout est celui des sub-state pour rester dans le même écran mais en y ajoutant des fonctionnalités.")])])}),[],!1,null,null,null);s.default=a.exports}}]);