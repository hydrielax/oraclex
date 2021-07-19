from .models import *
from django.db.models import Q
from math import sqrt
import datetime
from dateutil.relativedelta import relativedelta


# lecture des requêtes
# --------------------

def find_motsCles(mots):
    motsCles = []
    for mot in mots:
        matching_mot = Mot.objects.filter(name = mot)
        if matching_mot:
            motsCles.append(matching_mot[0].motcle.pk)
    return MotCle.objects.filter(pk__in=motsCles)

def firstDay(month, year):
    return datetime.date(int(year), int(month), 1)

def lastDay(month, year):
    date = firstDay(month, year)
    if not date: return date
    return date + relativedelta(months=1, days=-1)


# filtrage des jugements
# ----------------------

def filtrerJugements(motsCles, dateMin, dateMax, type_juridiction, juridiction):
    jugements = Jugement.objects.all()
    if motsCles:
        for motcle in motsCles:
            jugements = jugements.filter(mots_cles= motcle)
    if dateMin:
        jugements = jugements.filter(date_jugement__gte = dateMin)
    if dateMax:
        jugements = jugements.filter(date_jugement__lte = dateMax)
    if type_juridiction:
        jugements = jugements.filter(juridiction__type_juridiction = type_juridiction)
    if juridiction:
        jugements = jugements.filter(juridiction = juridiction)
    
    return jugements


# calculs des statistiques
# ------------------------

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