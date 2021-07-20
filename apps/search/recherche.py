from .models import *
from django.db.models import Q
from math import sqrt
import datetime
from dateutil.relativedelta import relativedelta
import math
import numpy as np


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
    if not month or not year: return None
    return datetime.date(int(year), int(month), 1)

def lastDay(month, year):
    date = firstDay(month, year)
    if not date: return None
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
    n = jugements.count()
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
    v = v / jugements.count()
    return sqrt(v)

def minimumGain(jugements):
    if not jugements:
        return None
    return min(jugements.values_list('gain', flat=True))

def maximumGain(jugements):
    if not jugements:
        return None
    return max(jugements.values_list('gain', flat=True))


# Création des graphiques
# -----------------------

def regroup_gains(jugements, n=10):
    gains = list(jugements.values_list('gain', flat=True))
    minGain = min(gains)
    maxGain = max(gains)
    if minGain < 0 and maxGain > 0:
        l = (maxGain - minGain) / (n-2)
        bornes_pre = list(np.arange(0, minGain-l, -l))
        bornes_pre.reverse()
        bornes_post = list(np.arange(0, maxGain+l, l))
        bornes_post[0] = 0.01
        bornes = bornes_pre + bornes_post
        print(bornes)
    else:
        bornes = list(np.linspace(minGain, maxGain, n+1))
    bornes = [math.floor(100*x)/100 for x in bornes]
    bornes[-1] += 0.01
    n = len(bornes)-1
    labels = [f'{bornes[i]} à {bornes[i+1]} €' for i in range(n)]
    data = [jugements.filter(gain__gte=bornes[i], gain__lt=bornes[i+1]).count() for i in range(n)]
    return labels, data
