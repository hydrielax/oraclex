# Pour exécuter ce code : 
# python3 manage.py shell
# from init_data import init_database
# init_database()

import csv
from apps.search.models import Juridiction, TypeJuridiction, MotCle, GroupeMotCle


def rangerMotCle():
    '''Modifie et range les indices des mots-clés pour la recherche, pour 
    faire correspondre les id aux indices du select de la liste à cocher.'''
    liste = MotCle.objects.all()
    #for motcle in MotCle.objects.all():
        #motcle.delete()
    for i in range(0, len(liste)):
        motcle = MotCle.objects.get(id=liste[i].id)
        motclesave = motcle
        motcle.delete()
        motclesave.id = i
        motclesave.save()


def import_mot_cle():
    '''Importe les mots-clés'''

    #on efface les mots-clés
    for motcle in MotCle.objects.all():
        motcle.delete()
    
    #on ajoute les mots clés depuis le fichier
    file = open('media/mots_cles.txt', 'r')
    for row in file:
        motcle = MotCle(
            nom = row,
        )
        motcle.save()


def import_type_juridiction():
    '''Initialise les différents types de cours'''

    #on efface tous les types
    for type in TypeJuridiction.objects.all():
        type.delete()

    #on les intialise
    TypeJuridiction(cle="CP", nom="Conseil des Prud'Hommes", niveau="1").save()
    TypeJuridiction(cle="CA", nom="Cour d'Appel",            niveau="2").save()
    TypeJuridiction(cle="CC", nom="Cour de Cassation",       niveau="3").save()


def import_cp():
    '''Importe dans la base de données la liste des Conseils de Prud'Hommes.'''

    #on efface tous les cp
    for cp in Juridiction.objects.filter(type_juridiction='CP'):
        cp.delete()

    #on les réimporte depuis le fichier
    file = open('media/Conseil_Prudhommes.csv', 'r')
    reader = csv.reader(file, delimiter=",")

    for row in reader:
        juridiction = Juridiction(
            nom = row[0], 
            ville = row[1],
            type_juridiction = TypeJuridiction.objects.get(cle='CP'),
            rattachement = None,
        )
        juridiction.save()

    file.close()


def import_ca():
    '''Importe dans la base de données la liste des Cours d'Appel.'''
    
    #on efface toutes les ca
    for ca in Juridiction.objects.filter(type_juridiction='CA'):
        ca.delete()

    #on les réimporte depuis le fichier
    file = open('media/Cour_Appel.csv', 'r')
    reader = csv.reader(file, delimiter=",")

    for row in reader:
        juridiction = Juridiction(
            nom = row[0], 
            ville = row[1],
            type_juridiction = TypeJuridiction.objects.get(cle='CA'),
            rattachement = None,
        )
        juridiction.save()

    file.close()


def import_cc():
    '''Importe dans la bdd la cour de Cassation'''

    Juridiction(
        nom="Cour de Cassation de Paris", 
        ville="Paris",
        type_juridiction=TypeJuridiction.objects.get(cle='CC'),
        rattachement = None,
    ).save()


def init_database():
    print('Importation des mots-clés...')
    import_mot_cle()
    print('Importation des juridictions...')
    import_type_juridiction()
    import_cp()
    import_ca()
    import_cc()
    print('Initialisation de la base de donnée terminée !')