# ORACLEX

*Un projet école-entreprise du groupe P2E46 : Karim CHAKROUN, Giovana LONGATTI BAPTISTA, Samy HAFFOUDHI, François MICHELON, Alexis DELAGE, Théodore RADU*

*En cas de besoin, contactez le chef de projet : [alexidelage@gmail.com](mailto:alexidelage@gmail.com).*


## Liens utiles

* [Tuto Django de Mozilla](https://developer.mozilla.org/fr/docs/Learn/Server-side/Django)
* [Documentation Django](https://docs.djangoproject.com/fr/3.2/)
* [Le Bootstrap SNCF](https://design-bootstrap.sncf.fr/fr/docs/4.3/getting-started/introduction/)
* [Le Bootstrap officiel](https://getbootstrap.com/docs/5.0/getting-started/introduction/)

## Démarrage rapide

* **Se créer un compte développeur :** dans l'onglet `shell` de *Repl.it*, tapez la commande `python3 manage.py createsuperuser`
* **Se connecter :** 
    1. Cliquer sur `Run` dans *Repl.it*.
    2. Le site s'ouvre alors en réduit.
    3. Cliquez sur l'icône à côté de la croix X pour l'ouvrir dans un nouvel onglet.
    4. Connectez-vous avec les identifiants créés précédemment
* **Accéder au site de gestion de la base de données :** ajouter `/admin` à la barre d'adresse dans l'onglet avec le site
* **Mettre à jour la base de données :** après avoir modifié un fichier `models.py`, il faut *migrer* la BDD : pour cela, tapez dans le shell de repl les commandes `python3 manage.py makemigrations` puis `python3 manage.py migrate`.

## Gestion des utilisateurs

Pour l'instant les utilisateurs se gèrent uniquement depuis l'interface admin. Il y a 2 groupes d'utilisateurs : les *Développeurs* et les *Membres du Service Juridique SNCF*.
Seules les *Développeurs* ont accès à l'interface admin.

## La base de données
Les tables créées corespondent aux `class` dans le fichier `app/forms.py`. Quelques précisions :
* La table `Jugement` représente un fichier de jugement : elle contient le fichier du jugement, les données extraites de ce fichier, ainsi que la date d'import du fichier et l'utilisateur qui l'a importé
* La table `Juridiction` représente le tribunal qui a jugé un certain jugement. Les différents tribunaux ont été importés à partir de l'[annuaire officiel](http://www.annuaires.justice.gouv.fr/annuaires-12162/annuaire-des-conseils-de-prudhommes-21779.html), via la [base de données de la justice](http://petitpois.justice.comarquage.fr/poi/search), avec les scripts du fichier `update_data.py`.
* Pour les différents types de juridiction, nous avons choisi de les importer sous forme d'une table `TypeJuridiction` pour prévoir l'ajout d'autres types facilement (notamment pour d'autres services juridiques de la SNCF qui s'appuient sur d'autres juridictions)
