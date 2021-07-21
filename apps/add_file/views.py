from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import ChoixFichiers
from .models import Jugement, JugementTemp
from apps.account.models import Agent
from itertools import chain

JugementTemp.thread.start()

@login_required
def ajout(request):
    if request.method == 'POST':
        fichiers = request.FILES.getlist('fichiers') + request.FILES.getlist('dossier')
        for f in fichiers:
            jugement = JugementTemp(file=f, agent_import=Agent.objects.get(user=request.user))
            jugement.save()
    return render(request, 'add_file/index.html', {'selection': ChoixFichiers()})


def send_history(request):
    agent = Agent.objects.get(user=request.user)
    jugements = chain(JugementTemp.objects.filter(agent_import=agent), Jugement.objects.filter(agent_import=agent))
    tableau = [{'date':'Date import', 'name':'Nom du fichier', 'state':'État'}]
    for jugement in jugements:
        date = '<span order="{0}">{1}</span>'.format(jugement.date_import, jugement.date_import.strftime("%d/%m/%Y"))
        name = '<a href="{0}">{1}</a>'.format(jugement.get_absolute_url(), jugement.name)
        if (type(jugement).__name__ == 'Jugement'): state = '<span order="1" class="text-dark">Validé</span>'
        elif jugement.doublon: state = '<span order="2" class="text-red">Doublon !</span>'
        else: state = '<span order="3" class="text-success">Analyse...</span>'
        tableau.append({"date": date, "name": name, "state": state})
    return JsonResponse(tableau, safe=False)
