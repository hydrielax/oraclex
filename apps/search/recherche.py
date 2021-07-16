from .models import *
from django.db.models import Q
from math import sqrt


def find_motsCles(mots):
    motsCles = []
    for mot in mots:
        matching_mot = Mot.objects.filter(name = mot)
        if matching_mot:
            motsCles.append(matching_mot[0].motcle.pk)
    return MotCle.objects.filter(pk__in=motsCles)


def filtrerJugements(motsCles, dateMin, dateMax, type_juridiction, juridiction):
    jugements = Jugement.objects.all()
    variables = {
        'mots_cle': motsCles,
        'date_jugement_min': dateMin,
        'date_jugement_max': dateMax,
        'type_juridiction': type_juridiction,
        'juridiction': juridiction,
    }
    for key, value in variables.items():
        if key == 'mots_cle' and value:
            jugements = jugements.filter(mots_cle__nom__in=motsCles).distinct()
        print(jugements)
        if key == 'date_jugement_min' and value:
            annee, mois = dateMin.split(" ")
            dateQuery = Q(date_jugement__year__gt=annee) | (Q(date_jugement__year=annee) & Q(date_jugement__month__gte=mois))
            jugements = jugements.filter(dateQuery)
        if key == 'date_jugement_max' and value:
            annee, mois = dateMax.split(" ")
            dateQuery = Q(date_jugement__year__lt=annee) | (Q(date_jugement__year=annee) & Q(date_jugement__month__lte=mois))
            jugements = jugements.filter(dateQuery)
        if key == 'type_juridiction' and value:
            jugements = jugements.filter(juridiction__type_juridiction = type_juridiction)
        if key == 'juridiction' and value:
            jugements = jugements.filter(juridiction__nom=juridiction)
    
    return jugements.order_by('gain')

def moyenneGains(jugements):
    if not jugements:
        return None
    s = 0
    n = 0
    for jugement in jugements:
        s += jugement.gain
        n += 1
    return s / n

def medianeGains(jugements):
    n = len(jugements)
    if n % 2 == 1:
        return jugements[n//2].gain
    elif n > 0:
        return (jugements[n // 2 - 1].gain + jugements[n // 2].gain) / 2
    else:
        return None

def ecart_type_gains(jugements):
    if not jugements:
        return None
    v = 0
    m = moyenneGains(jugements)
    for jugement in jugements:
        v += (jugement.gain - m) ** 2
    v = v / len(jugements)
    return sqrt(v)

def minimumGain(jugements):
    if not jugements:
        return None
    return min([jugement.gain for jugement in jugements])

def maximumGain(jugements):
    if not jugements:
        return None
    return max([jugement.gain for jugement in jugements])