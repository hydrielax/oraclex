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
2. Ouvrez un terminal Linux (de préférence dans VScode, ou ailleurs si vous voulez). Si vous utilisez la ligne de commande Windows ou macOS, référez-vous à la section dédiée ci-dessous. Sous Windows, nous vous recommendons de plutôt installer WSL pour pouvoir utiliser directement la ligne de commande Linux.
3. Installez *Python*, *pip3*, et *virtualenvwrapper* (en cas de besoin, utilisez la [documentation de MDN](https://developer.mozilla.org/fr/docs/Learn/Server-side/Django/development_environment))
4. Créez un environnement virtuel nommé **oraclex_env** avec la commande `mkvirtualenv oraclex_env`. Vous devrez voir apparaître `(oraclex_env)` au début de vos lignes de commande ensuite (si ce n'est pas le cas, tapez `workon oraclex_env`)
5. Placez-vous dans le dossier `oraclex` avec la commande `cd` si besoin
6. Installez les dépendances logicielles : `sudo apt-get install $(cat Aptfile)`
6. Installez les dépendances Python : `pip3 install -r requirements.txt`
7. Créez la base de données : `python3 manage.py migrate` 
8. Remplissez la BDD avec les données de base :
    ```python
    python3 manage.py shell
    >> from init_data import init_database
    >> init_database()
    ```
9. Créez un compte super-utilisateur : `python3 manage.py createsuperuser`


---

> ### Instructions propres à MacOS
> * **Installer tesseract-OCR :** 
>   * Installer la package : `sudo port install tesseract`
>   * Installer le module pourle Français : `sudo port install tesseract-fra`
> * **Installer poppler :**
>   * Vous devrez installer poppler pour Mac : http://macappstore.org/poppler/

---

> ### Instructions propres à la ligne de commande Windows
> 
>> * **Python :**
>>   * **Exécution de python :** remplacez partout `python3` par `py -3`
>>   * **En cas d'erreur de modules Python non importés :** ajoutez le path d'accès avec la commande `export PYTHONPATH="${PYTHONPATH}:/path/to/your/project/"` (`set PYTHONPATH=%PYTHONPATH%;C:\path\to\your\project\` ou `set export PYTHONPATH="${PYTHONPATH}:/path/to/your/project/` pour Windows) puis fermez le terminal et réessayez, ou bien faites un import absolu (en dehors de l'environnement virtuel)
>
>> * **Pour installer Tesseract-OCR :**
>>   1. Respirez profondément, il faudra un peu de patience ici.
>>   2. Installez tesseract à l'aide du programme d'installation Windows disponible à l'adresse suivante : https://github.com/UB-Mannheim/tesseract/wiki
>>   3. Notez le chemin d'accès à tesseract depuis l'installation. Le chemin d'installation par défaut généralement est : `C:\Users\USER\AppData\Local\Tesseract-OCR`ou bien `C:\Program Files\Tesseract-OCR` Il est possible qu'il change, veuillez donc vérifiez le chemin d'installation.
>>   4. Ajouter le Path avec : Modifier les variables d'environnement système >> Variables d'environnement... >> Variable : Path >> Modifier >> Nouveau >> Ajouter le chemin d'accès et enregistrer.
>>
>>  Si cela n'a pas fonctionné, essayez l'une de ces solutions : 
>>   * Chocolatey : 
>>       1. Installez chocolatey avec powershell.exe : 
`Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))`
>>       2. Puis utilisez la commande suivante :
`choco install tesseract --pre `
>>       3. Le programme d'installation de Tesseract fourni par Chocolatey ne comprend actuellement que la langue anglaise. Pour installer la langue française, téléchargez le pack de langue correspondant (fichier fra.traineddata) à partir de https://github.com/tesseract-ocr/tessdata/ et placez-le dans `C:\Program Files\Tesseract-OCR\tessdata` (ou à l'endroit où Tesseract OCR est installé).
>>
>> * Anaconda : 
>>     1. Installez Anaconda. 
>>     3. Puis avec Anaconda prompt utilisez la commande suivante :
`conda install -c conda-forge tesseract `
>>
>> * Changer le code : 
>>     * **C'est la dernière solution, que nous ne recommandons pas vraiment, qui consiste à changer le code, cela ne fonctionnera pas pour le serveur, mais seulement dans le local.**
>>     5. Après l'étape 4. Dans votre code, mettez le chemin de tesseract avant d'appeler image_to_string :
`pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'` (ou le chemin que vous aviez.)
>
>> * **Pour installer Poppler sur Windows :**
>>      1. Allez sur cette page : http://blog.alivate.com.au/poppler-windows/  et téléchargez le binaire de votre choix, ou bien utilisez ce lien direct : http://blog.alivate.com.au/wp-content/uploads/2018/10/poppler-0.68.0_x86.7z
>>      2. Extrayez le fichier d'archive `poppler-0.68.0_x86.7z` dans `C:\Program Files`. Ainsi, la structure du répertoire devrait ressembler à ceci :
>>      ```
>>      C :
>>          └ Program Files
>>              └ poppler-0.68.0_x86
>>                  └ bin
>>                  └ include
>>                  └ lib
>>                  └ share
>>      ```
>>      3. Ajoutez `C:\Program Files\poppler-0.68.0_x86\bin` à votre PATH système en procédant comme suit : 
>>          * Cliquez sur le bouton *Démarrer* de Windows, et recherchez *Modifier les variables*
>>          * Modifier les variables d'environnement du système >> sur Variables d'environnement...>> PATH >> Nouveau >> puis ajoutez `C:\Users\Program Files\poppler-0.68.0_x86\bin`,et enregistrez.
>>
>> Autres solutions plus simple : 
>> * Chocolatey : `choco install poppler`
>> * Anaconda : `conda install -c conda-forge poppler`
>>
>

---
## Commandes courantes

* **À chaque fois que vous revenez sur le code,** il faut relancer l'environnement virtuel avec la commande : `workon oraclex_env`
* **Pour tester le site en local :**
    1. Placez-vous dans le dossier `oraclex` avec `cd` si besoin
    2. Vérifiez que l'environnement virtuel est activé
    3. Lancez le serveur : `python3 manage.py runserver`
    4. Dans un navigateur, connectez-vous à l'adresse **http://localhost:8000**
    5. Pour arrêter le serveur, tapez `CTRL+C`
* **Lorsque vous modifiez la structure de la base de donnée** (fichiers `models.py`) :
    1. Vérifiez que le serveur est arrêté
    2. Créez un script de migration de l'ancienne bdd à la nouvelle : `python3 manage.py makemigrations`
    3. Appliquez les changements : `python3 manage.py migrate`

---

## Documentation

Pour voir la documentation relative au projet, des schémas expliquant le fonctionnement des principales parties sont disponibles dans le dossier `doc`. Des commentaires sont aussi ajoutés dans le code afin de mieux suivre les différents choix faits.
Attention, avant de vous plonger dans le code, il est fortement conseillé de faire le tuto Django (mentionné en haut de cette page) auparavant.