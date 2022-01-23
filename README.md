### PRESENTATION ET OBJECTIFS DE L'APPLICATION

Ce projet a été développée avec le famework Django, sur une architecture de projet MVT donc. 
Le projet se décompose en deux applications : User qui gère toutes les vues, templates et modèles relatifs aux utilisateurs, et Administration, qui regroupe
toutes les fonctionnalités relatives à la gestion des clients, réservations, animaux en base de données, la consultation des statistiques etc... Le SGBDR retenu pour ce projet a
été PostGreSQL, notamment pour sa facilité de déploiement sur serveur et sa facilité d'emploi avec le Framework utilisé. Le serveur web utilisé est Gunicorn ( comme détaillé dans
le procfile ), le serveur de développement celui intégré à Django. Les requêtes en base de données sont réalisées avec l'ORM de Django. La partie
frontend utilise le framework CSS Bootstrap4 avec une intégration au projet de type CDN. L'interface logique entre le front et le back utilise à la
fois les possibilités offertes par le moteur de template de Django ( à savoir l'intégration d'instrctions python directement dans les templates ), et
des fonctions rédigées en JS ( sans surcouche ), pour les eventlistener notamment. Le programme utilise également l'API d'OpenFoodFacts, au sein de
différentes fonctionnalités.

Ce projet a été réalisé pour les besoins d’une pension canine en phase de développement. Il répond à un besoin de centralisation des éléments 
de gestion de l’entreprise, ainsi qu’à un désir d’accéder de manière simple et rapide à l’ensemble des opérations quotidiennes nécessaires à la gestion de l’entreprise.
L’application s’adresse essentiellement au personnel de la pension mais également, dans une moindre mesure, aux clients eux même, qui bénéficient d’un certain nombre de services via cette même plateforme.

---

### PREREQUIS

Pour exécuter convenablement le programme, il faut préparer l'environnement pour que tout se passe correctement. Il faut donc :

* Cloner le repo GitHub du projet, ce qui est soit faisable en faisant un téléchargement manuel depuis GitHub, soit en utilisant **Git Bash** ( les
procédures de clonnage sont facilement trouvables sur google ).

* Initialiser un environnement virtuel ( avec **Virtual Env** par exemple ). Dans ce cas, il vous faudra créer votre environnement virtuel avec
**Python 3** dessus, puis l'activer. Selon que vous soyez sous Windows, MacOS ou Linux, les procédures changent légèrement. Là encore, elles sont très
facilement trouvables sur Google.

* Pour éxecuter le programme, il est nécessaire d'installer les librairies requises. Pour cela, on peut tout simplement utiliser _PIP_ pour
installer toutes les librairies qui figurent dans le **requirements.txt**, via la commande _pip install * requirements.txt_. Cette commande est
à exécuter à la racine du projet, en ayant bien son environnement virtuel activé !!!

* Enfin, il vous sera nécessaire de définir une nouvelle variable d'environnement sur votre machine, appellée ENV, à laquelle vous assignerez la
valeur de votre choix, excepté "PRODUCTION". Cela déterminera si le mode débug est actif ou non lors de l'éxécution du programme, le but étant qu'il
soit actif sur serveur de développement...

---

### EXECUTION DU PROGRAMME

Après avoir installé les librairies, il faudra effectuer les migrations des modèles afin d'initialiser la structure de la base de données. Pour celà,
exécutez la commande Django _python manage.py migrate_ dans votre console à la racine du projet. Une fois cela fait, exécutez les migrations avec la
commande _python manage.py makemigrations_. La base de données est maintenant initialisée, et il va falloir la remplir. Pour celà, exécutez la commande
personnalisée Django _python manage.py database_init_, toujours à la racine du projet. Cette commande va prendre un certain temps à s'exécuter, car
elle va réaliser plusieurs appels à l'API d'OpenFoodFacts. Ensuite, exécutez la commande _python manage.py runserver_ dans votre console à la racine 
du projet toujours ( sous windows ). _Django_ utilisera alors son serveur de développement intégré pour vous proposer une URL sur le port 8000 par 
défaut ( typiquement de type _http://127.0.0.1:8000/_ ). Vous pourrez alors accéder à l'interface utilisateur en suivant cette URL.

---

### EXECUTION DES TESTS

Si vous souhaitez lancer les tests, il vous faudra lancer le serveur de développement de Django dans un terminal en exécutant la commande 
_python manage.py runserver_ à la racine du projet ( et en veillant bien à avoir son environnement virtuel d'activé ), puis exécuter la commande 
_python manage.py test_ à la racine du projet depuis un second terminal. Cela lancera l'exécution des tests unitaires avec **TestCase** et des tests 
de parcours utilisateur avec **selenium**. De ce fait, ASSUREZ-VOUS D'AVOIR INSTALLE LES DRIVERS DE GOOGLE CHROME disponnibles à 
[cette adresse](https://sites.google.com/a/chromium.org/chromedriver/). Ajoutez ensuite le chemin vers le driver à votre variable d'environnement 
_PATH_, en suivant la [procédure suivante](https://zwbetz.com/download-chromedriver-binary-and-add-to-your-path-for-automated-functional-testing/).

