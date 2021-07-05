from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import RequeteForm
from apps.search.models import Jugement, MotCle, GroupeMotCle
from .recherche import *


@login_required
def recherche(request):
    if request.method == 'POST':
        form = RequeteForm(request.POST)
        if form.is_valid():
            try:
                request.session['type_juridiction'] = form.cleaned_data['type_juridiction'].nom
            except:
                request.session['type_juridiction'] = None
            try:
                request.session['juridiction'] = form.cleaned_data['juridiction'].nom
            except:
                request.session['juridiction'] = None
            try:
                request.session['dateMin'] = form.cleaned_data['dateMin'].strftime("%Y %m")
            except:
                request.session['dateMin'] = None
            try:
                request.session['dateMax'] = form.cleaned_data['dateMax'].strftime("%Y %m")
            except:
                request.session['dateMax'] = None
            motsCles = list(set([mot.nom for mot in form.cleaned_data['motsCles']] + [m.upper() for m in form.cleaned_data['motsCles_textInput'].split(",")]))
            #motsCles.remove('')
            request.session['motsCles'] = motsCles
            return redirect('search:results')
    else:
        form = RequeteForm()

    indexmotcles = MotCle.objects.all()
    groupes = GroupeMotCle.objects.all()
    liste = []
    for i in range(0, len(groupes)):
        listeMotCle = []
        mots_cles = MotCle.objects.filter(groupe=groupes[i])
        for motcle in mots_cles:
            index=0
            #while indexmotcles[index]!=motcle: index+=1
            listeMotCle.append({'id': motcle.id, 'nom': motcle.nom, })
        liste.append({'id':i, 'nom': groupes[i].nom, 'mots_cles': listeMotCle, })
    
    #en 2 : mots-clés sans groupes
    liste2 = []
    mots_cles = MotCle.objects.filter(groupe__isnull=True)
    for motcle in mots_cles:
        index=0
        #while indexmotcles[index]!=motcle: index+=1
        liste2.append({'id': motcle.id, 'nom': motcle.nom, })

    context = {
        'form': form, 
        'liste': liste,
        'liste_sans_groupe': liste2,
    }

    return render(request, 'search/index.html', context)


@login_required
def resultat(request):
    # recuperation des donnees saisies
    type_juridiction = request.session['type_juridiction']
    juridiction = request.session['juridiction']
    dateMin = request.session['dateMin']
    dateMax = request.session['dateMax']
    motsCles = request.session['motsCles']

    parametres = {
        'dateMin': dateMin,
        'dateMax': dateMax,
        'motsCles': motsCles,
        'juridiction': juridiction,
        'type_juridiction': type_juridiction,
    }

    jugements = filtrerJugements(motsCles, dateMin, dateMax, type_juridiction, juridiction)

    # recuperation des donnes a partir des scripts
    moyenne = moyenneGains(jugements)
    ecart_type = ecart_type_gains(jugements)
    mediane = medianeGains(jugements)
    minimum = minimumGain(jugements)
    maximum = maximumGain(jugements)

    stats = {
        'moyenne': moyenne,
        'ecart_type': ecart_type,
        'mediane': mediane,
        'minimum': minimum,
        'maximum': maximum,
    }

    # graphique répartitions des gains
    labels = sorted(list(set([jugement.gain for jugement in jugements])))
    data = [len(jugements.filter(gain=x)) for x in labels]

    graph_gain = {
        'labels': labels,
        'data': data
    }

    graph_pie = {
       'labels' : ["favorable", "défavorable"],
       'data': [len(jugements.filter(gain__gte=0)), len(jugements.filter(gain__lt=0))]
    }

    return render(request, 'search/resultat.html', {
        'parametres': parametres,
        'jugements': jugements,
        'stats': stats,
        'graph_gain': graph_gain,
        'graph_pie': graph_pie
    })




@login_required
def unreadables(request):
    '''Génère la liste des Fichiers Illsibles.'''

    # fichiers illisibles
    bad_files = Jugement.objects.filter(lisible = False).all()

    context = {
        'bad_files': bad_files,
    }
    return render(request, 'search/unreadables.html', context)