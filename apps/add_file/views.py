from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ChoixFichiers, Historique
from .models import JugementTemp
from apps.search.models import Jugement
from apps.account.models import Agent
from itertools import chain
from threading import Thread


@login_required
def ajout(request):
    agent = Agent.objects.get(user=request.user)
    if request.method == 'POST':
        fichiers = request.FILES.getlist('fichiers')
        for f in fichiers:
            jugement = JugementTemp(file=f, agent_import=agent)
            analyse = Thread(target=jugement.analyse)
            analyse.start()
    selection = ChoixFichiers()
    historique = chain(JugementTemp.objects.filter(agent_import=agent), Jugement.objects.filter(agent_import=agent))
    tableau = Historique(historique)
    print(tableau)
    context = {'selection': selection, 'tableau': tableau}
    return render(request, 'add_file/index.html', context)
