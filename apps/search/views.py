from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from .forms import RequeteForm
from .models import Jugement
from .recherche import *
from apps.add_file.models import JugementTemp


@login_required
def searchview(request):
    '''Vue pour la recherche et les résultats'''
    context = {}
    if request.GET:
        form = RequeteForm(request.GET)
        form.full_clean()
        if request.GET.getlist('motcle'):
            form.cleaned_data['motcle'] = request.GET.getlist('motcle')
            del form._errors['motcle']
        if form.is_valid():
            context = show_results(form)
    else:
        form = RequeteForm(initial={'datemMax': datetime.datetime.now().month})

    context['form'] = form
    return render(request, 'search/index.html', context)



def show_results(form):
    '''Afficher les résultats de la recherche'''

    # récupérer les résultats
    motsCles = find_motsCles(form.cleaned_data['motcle'])
    dateMin = firstDay(form.cleaned_data['datemMin'], form.cleaned_data['dateyMin'])
    dateMax = lastDay(form.cleaned_data['datemMax'], form.cleaned_data['dateyMax'])
    type_juridiction = form.cleaned_data['type_juridiction']
    juridiction = find_juridiction(form.cleaned_data['juridiction'])
    illisibles = form.cleaned_data['illisibles']
    jugements = filtrerJugements(motsCles, dateMin, dateMax, type_juridiction, juridiction,illisibles)
    jugements = jugements.order_by('gain')

    stats, graph_gain, graph_pie = None, None, None

    if jugements:
        # statistiques
        list_jugements = jugements.filter(gain__isnull=False)
        if list_jugements:
            stats = {
                'moyenne': moyenneGains(list_jugements),
                'ecart_type': ecart_type_gains(list_jugements),
                'mediane': medianeGains(list_jugements),
                'minimum': minimumGain(list_jugements),
                'maximum': maximumGain(list_jugements),
            }

        # graphiques
        graph_pie = {
        'labels' : ["Favorable ", "Mixte ", "Défavorable ", "Inconnu "],
        'data': [
                jugements.filter(decision='F').count(), 
                jugements.filter(decision='M').count(), 
                jugements.filter(decision='D').count(),
                jugements.filter(decision__isnull=True).count(),
            ],
        }

        if list_jugements:
            labels, data = regroup_gains(list_jugements)
            graph_gain = {
                'labels': labels,
                'data': data,
            }

    # envoie au template
    context = {
        'jugements': jugements,
        'stats': stats,
        'graph_gain': graph_gain,
        'graph_pie': graph_pie,
        'nb_results': jugements.count(),
        'nb_illisibles': jugements.filter(lisible=False).count(),
        'show_illisibles': illisibles,
        'motsCles': motsCles,
    }
    return context


@login_required
def unreadables(request):
    '''Génère la liste des Fichiers Illsibles.'''

    # fichiers illisibles
    bad_files = Jugement.objects.filter(lisible = False).all()

    context = {
        'bad_files': bad_files,
    }
    return render(request, 'search/unreadables.html', context)


@login_required
def detailsview(request, id, temp=False):
    if temp:
        jugement = JugementTemp.objects.get(id=id)
    else:
        jugement = Jugement.objects.get(id=id)
    return render(request, 'search/details.html', {'jugement':jugement})


@login_required
def detailstempview(request, id):
    return detailsview(request, id, True)