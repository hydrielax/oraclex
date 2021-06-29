# ORACLEX

*Contributeurs du projet : Karim CHAKROUN, Giovana LONGATTI BAPTISTA, Samy HAFFOUDHI, François MICHELON, Alexis DELAGE, Théodore RADU, Anass AL AMMIRI*

*Contact : [alexidelage@gmail.com](mailto:alexidelage@gmail.com).*

Oraclex est un projet de gestion, d'analyse, et de prédiction de décisions de justice. 

---

## Liens utiles

* [Tuto Django de Mozilla](https://developer.mozilla.org/fr/docs/Learn/Server-side/Django)
* [Documentation Django](https://docs.djangoproject.com/fr/3.2/)
* [Le Bootstrap SNCF](https://design-bootstrap.sncf.fr/fr/docs/4.3/getting-started/introduction/)
* [Le Bootstrap officiel](https://getbootstrap.com/docs/5.0/getting-started/introduction/)

---

## Installation

1. Clonez le repo Github sur votre ordinateur et ouvrez-le dans *Visual Studio Code* à partir du logiciel *Github Desktop*
2. Ouvrez un terminal (de préférence dans VScode, ou ailleurs si vous voulez)
3. Installez *Python*, *pip3*, et *virtualenvwrapper* (en cas de besoin, utilisez la [documentation de MDN](https://developer.mozilla.org/fr/docs/Learn/Server-side/Django/development_environment))
4. Créez un environnement virtuel nommé **oraclex_env** avec la commande `$ mkvirtualenv oraclex_env`. Vous devrez voir apparaître `(oraclex_env)` au début de vos lignes de commande ensuite (si ce n'est pas le cas, tapez `$ workon oraclex_env`)
5. Placez-vous dans le dossier `oraclex` avec la commande `cd` si besoin
6. Installez les dépendances : `$ pip3 install -r requirements.txt`
7. Créez la base de données : `$ python3 manage.py migrate`
8. Remplissez la BDD avec les données de base :
    ```python
    $ python3 manage.py shell
    >>> from init_data import init_database
    >>> init_database()
    ```
9. Créez un compte super-utilisateur : `$ python3 manage.py createsuperuser`

---

## Commandes courantes

* **À chaque fois que vous revenez sur le code,** il faut relancer l'environnement virtuel avec la commande : `$ workon oraclex_env`
* **Pour tester le site en local :**
    1. Placez-vous dans le dossier `oraclex` avec `cd` si besoin
    2. Vérifiez que l'environnement virtuel est activé
    3. Lancez le serveur : `$ python3 manage.py runserver`
    4. Dans un navigateur, connectez-vous à l'adresse **http://localhost:8000**
    5. Pour arrêter le serveur, tapez `CTRL+C`
* **Lorsque vous modifiez la structure de la base de donnée** (fichiers `models.py`) :
    1. Vérifiez que le serveur est arrêté
    2. Créez un script de migration de l'ancienne bdd à la nouvelle : `$ python3 manage.py makemigrations`
    3. Appliquez les changements : `$ python3 manage.py migrate`

---

## Documentation

### Gestion des utilisateurs

Pour l'instant les utilisateurs se gèrent uniquement depuis l'interface admin. Il y a 2 groupes d'utilisateurs : les *Développeurs* et les *Membres du Service Juridique SNCF*.
Seules les *Développeurs* ont accès à l'interface admin.

### La base de données
Les tables créées corespondent aux `class` dans le fichier `app/forms.py`. Quelques précisions :
* La table `Jugement` représente un fichier de jugement : elle contient le fichier du jugement, les données extraites de ce fichier, ainsi que la date d'import du fichier et l'utilisateur qui l'a importé
* La table `Juridiction` représente le tribunal qui a jugé un certain jugement. Les différents tribunaux ont été importés à partir de l'[annuaire officiel](http://www.annuaires.justice.gouv.fr/annuaires-12162/annuaire-des-conseils-de-prudhommes-21779.html), via la [base de données de la justice](http://petitpois.justice.comarquage.fr/poi/search)
* Pour les différents types de juridiction, nous avons choisi de les importer sous forme d'une table `TypeJuridiction` pour prévoir l'ajout d'autres types facilement (notamment pour d'autres services juridiques de la SNCF qui s'appuient sur d'autres juridictions)
* Les `MotCle` associés à un `Jugement` sont aussi répartis dans des groupes `GroupeMotCle`
