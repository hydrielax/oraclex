# Pour exécuter ce code : dans le shell, tapez :
# python3 manage.py shell
# from update_data import *

# fichiers déjà importés, ne plus les exécuter !!
# à conserver uniquement comme modèle si besoin

import csv
from app.models import Juridiction, TypeJuridiction, MotCle, GroupeMotCle

def rangerMotCle():
    '''Modifie et range les indices des mots-clés pour la recherche.'''
    liste = MotCle.objects.all()
    #for motcle in MotCle.objects.all():
        #motcle.delete()
    for i in range(0, len(liste)):
        motcle = MotCle.objects.get(id=liste[i].id)
        motclesave = motcle
        motcle.delete()
        motclesave.id = i
        motclesave.save()

def import_cp():
    '''Importe dans la base de données la liste des Conseils de Prud'Hommes.'''

    file = open('media/Conseil_Prudhommes.csv', 'r')
    reader = csv.reader(file, delimiter=",")

    for row in reader:
        juridiction = Juridiction(
            nom = row[0], 
            ville = row[1],
            type_juridiction = TypeJuridiction.objects.get(cle='CP'),
            rattachement = None,
        )
        #juridiction.save()

    file.close()


def import_ca():
    '''Importe dans la base de données la liste des Cours d'Appel.'''

    file = open('media/Cour_Appel.csv', 'r')
    reader = csv.reader(file, delimiter=",")

    for row in reader:
        juridiction = Juridiction(
            nom = row[0], 
            ville = row[1],
            type_juridiction = TypeJuridiction.objects.get(cle='CA'),
            rattachement = None,
        )
        #juridiction.save()

    file.close()
