from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import ChoixFichiers, AjoutMotCleForm
from .models import Jugement, JugementTemp
from apps.account.models import Agent
from itertools import chain

# AJOUT JUGEMENT
# --------------

JugementTemp.thread.start()

@login_required
def ajout(request):
    if request.method == 'POST':
        fichiers = request.FILES.getlist('fichiers') + request.FILES.getlist('dossier')
        for f in fichiers:
            jugement = JugementTemp(file=f, agent_import=Agent.objects.get(user=request.user))
            jugement.save()
    return render(request, 'add_file/index.html', {'selection': ChoixFichiers()})

@login_required
def send_history(request):
    agent = Agent.objects.get(user=request.user)
    jugements = chain(JugementTemp.objects.filter(agent_import=agent), Jugement.objects.filter(agent_import=agent)[:50])
    tableau = [{'date': 'Importé', 'name': 'Nom du fichier', 'state': 'État'}]
    for jugement in jugements:
        date = '<span order="{0}">{1}</span>'.format(jugement.date_import, jugement.date_import.strftime("%d/%m/%Y"))
        name = '<a href="{0}">{1}</a>'.format(jugement.get_absolute_url(), jugement.name)
        if (type(jugement).__name__ == 'Jugement'): state = '<span order="1" class="text-dark">Validé</span>'
        elif jugement.doublon: state = '<span order="2" class="text-red">Doublon !</span>'
        else: state = '<span order="3" class="text-success">Analyse...</span>'
        tableau.append({"date": date, "name": name, "state": state})
    return JsonResponse(tableau, safe=False)

# DOUBLONS
# --------

@login_required
def gestion_doublons(request):
    '''Vue pour gérer les doublons'''
    jugements = JugementTemp.objects.filter(doublon__isnull=False)
    return render(request, 'add_file/doublons.html', {'jugements': jugements})

@login_required
def keep_old(request, id):
    '''Action de doublon : conserver l'ancien'''
    jugement = JugementTemp.objects.get(id=id)
    jugement.delete()
    return redirect('add_file:doublons')

@login_required
def keep_new(request, id):
    '''Action de doublon : conserver le nouveau'''
    jugement = JugementTemp.objects.get(id=id)
    jugement.doublon.delete()
    jugement.register()
    return redirect('add_file:doublons')

@login_required
def keep_both(request, id):
    '''Action de doublon : conserver les deux'''
    jugement = JugementTemp.objects.get(id=id)
    jugement.register()
    return redirect('add_file:doublons')

# AJOUT MOT-CLE
# -------------

@login_required
def add_keyword(request):
    context = {}
    if request.method == 'POST':
        form = AjoutMotCleForm(request.POST)
        if form.is_valid():
            form.save()
            form = AjoutMotCleForm()
            context['ok'] = True
    else:
        form = AjoutMotCleForm()
    context['form'] = form
    return render(request, 'add_file/add_keyword.html', context)