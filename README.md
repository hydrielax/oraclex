# ORACLEX

*Un projet école-entreprise du groupe P2E46 : Karim CHAKROUN, Giovana LONGATTI BAPTISTA, Samy HAFFOUDHI, François MICHELON, Alexis DELAGE, Théodore RADU*

*En cas de besoin, contactez le chef de projet : [alexidelage@gmail.com](mailto:alexidelage@gmail.com).*


## Liens utiles

* [Tuto Django de Mozilla](https://developer.mozilla.org/fr/docs/Learn/Server-side/Django)
* [Documentation Django](https://docs.djangoproject.com/fr/3.2/)
* [Le Bootstrap SNCF](https://design-bootstrap.sncf.fr/fr/docs/4.3/getting-started/introduction/)
* [Le Bootstrap officiel](https://getbootstrap.com/docs/5.0/getting-started/introduction/)

## Installation

1. Clonez le repo Github sur votre ordinateur et ouvrez-le dans *Visual Studio Code* à partir du logiciel *Github Desktop*
3. Configurez votre ordinateur : [Explications de MDN](https://developer.mozilla.org/fr/docs/Learn/Server-side/Django/development_environment) - Attention ! Ne créez pas de nouveau projet dans le projet existant **oraclex** pour le test
2. Placez-vous dans le dossier `oraclex` (celui avec le fichier `manage.py`) : `cd oraclex`
4. Une fois l'environnement virtuel démarré, (s'il ne l'est pas déjà cf plus bas), 
## Gestion des utilisateurs

Pour l'instant les utilisateurs se gèrent uniquement depuis l'interface admin. Il y a 2 groupes d'utilisateurs : les *Développeurs* et les *Membres du Service Juridique SNCF*.
Seules les *Développeurs* ont accès à l'interface admin.

## La base de données
Les tables créées corespondent aux `class` dans le fichier `app/forms.py`. Quelques précisions :
* La table `Jugement` représente un fichier de jugement : elle contient le fichier du jugement, les données extraites de ce fichier, ainsi que la date d'import du fichier et l'utilisateur qui l'a importé
* La table `Juridiction` représente le tribunal qui a jugé un certain jugement. Les différents tribunaux ont été importés à partir de l'[annuaire officiel](http://www.annuaires.justice.gouv.fr/annuaires-12162/annuaire-des-conseils-de-prudhommes-21779.html), via la [base de données de la justice](http://petitpois.justice.comarquage.fr/poi/search), avec les scripts du fichier `update_data.py`.
* Pour les différents types de juridiction, nous avons choisi de les importer sous forme d'une table `TypeJuridiction` pour prévoir l'ajout d'autres types facilement (notamment pour d'autres services juridiques de la SNCF qui s'appuient sur d'autres juridictions)
