# Projet_IoT
Création et gestion d'une base de données via un site.

Description :
Le but de ce projet est de créer une base de données SQLite puis un site capable d'intéragir avec elle.

Liste des  dépendances :
git clone https://github.com/...
cd ...
pip install fastapi sqlite3 pydantic httpx
npm install express cors
npm install -g nodemon



 ==> Partie 1 : Base de données

Lancer application FastAPI avec le serveur HTTP Uvicorn : 
-> uvicorn serveur:app --reload

/!\ Exécuter logement.sql, qui réinitialise la base de données : 
Lancer depuis bon répertoire : 
-> sqlite3 logement.db
Lire le fichier :  
-> .read logement.sql

Toutes les questions sur cette partie se trouvent dans le fichier logement.sql.



==> Partie 2 : Serveur RESTful

Toutes les questions sur cette partie se trouvent dans le fichier serveur.py
et sont vérifiables très simplement en se rendant aux adresses tel que 
/logements
/camembert/{adresse} 
/meteo
…
La partie ESP n'a pas pu être effectuée



 ==> Partie 3 : Informations sur la partie HTML/CSS/Javascript

Connecter à la base de données SQLite grâce au serveur.js, depuis le bon répertoire : 
 -> node serveur.js
Pour éviter de relancer à chaque modification :
 -> nodemon serveur.js 

Mon projet permet entre autres de faire les actions suivantes
Modification base de données : numéro de téléphone sur la dernière page
Ajout dans la base de données : ajout de capteurs en dernière page
Lecture de la base de données : différents graphiques sur tout le site



Sources :
Tout le code vient de mes recherches personnelles.
Mes sources principales ont été les suivantes.
https://cloud.google.com/
https://chatgpt.com/
https://openclassrooms.com/
https://developer.mozilla.org/
https://www.youtube.com/
https://www.w3schools.com/
https://www.developpez.net/
https://www.codethemap.fr/
https://learn.microsoft.com/

