from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ChoixFichiers, Historique
from .models import Jugement, JugementTemp
from apps.account.models import Agent
from itertools import chain

JugementTemp.thread.start()

@login_required
def ajout(request):
    agent = Agent.objects.get(user=request.user)
    if request.method == 'POST':
        fichiers = request.FILES.getlist('fichiers')
        for f in fichiers:
            jugement = JugementTemp(file=f, agent_import=agent)
            jugement.save()
    selection = ChoixFichiers()
    jugements = chain(JugementTemp.objects.filter(agent_import=agent), Jugement.objects.filter(agent_import=agent))
    tableau = Historique(jugements)
    context = {'selection': selection, 'tableau': tableau}
    return render(request, 'add_file/index.html', context)
