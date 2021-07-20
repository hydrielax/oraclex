from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from .forms import ChoixFichiers
from .models import Jugement, JugementTemp
from apps.account.models import Agent
from itertools import chain

JugementTemp.thread.start()

@login_required
def ajout(request):
    agent = Agent.objects.get(user=request.user)
    if request.method == 'POST':
        fichiers = request.FILES.getlist('fichiers') + request.FILES.getlist('dossier')
        for f in fichiers:
            jugement = JugementTemp(file=f, agent_import=agent)
            jugement.save()
    selection = ChoixFichiers()
    jugements = chain(JugementTemp.objects.filter(agent_import=agent), Jugement.objects.filter(agent_import=agent))
    tableau = Historique(jugements)
    context = {'selection': selection, 'tableau': tableau}
    return render(request, 'add_file/index.html', context)


def update(request):
    agent = Agent.objects.get(user=request.user)
    jugements = chain(JugementTemp.objects.filter(agent_import=agent), Jugement.objects.filter(agent_import=agent))
    tableau = Historique(jugements)
    return JsonResponse({'tableau': tableau.__str__()})


class Historique(list):

    def __str__(self):
        js = '[{"date":"Date import", "name":"Nom du fichier", "state":"État"}'
        for jugement in self:
            date = '<span order=\\"{0}\\">{1}</span>'.format(jugement.date_import, jugement.date_import.strftime("%d/%m/%Y"))
            name = '<a href=\\"{0}\\">{1}</a>'.format(jugement.get_absolute_url(), jugement.name)
            if (type(jugement).__name__ == 'Jugement'): state = '<span order=\\"1\\" class=\\"text-dark\\">Validé</span>'
            elif jugement.doublon: state = '<span order=\\"2\\" class=\\"text-red\\">Doublon !</span>'
            else: state = '<span order=\\"3\\" class=\\"text-success\\">Analyse...</span>'
            js += ', {{"date":"{0}", "name":"{1}", "state":"{2}"}}'.format(date, name, state)
        js += "]"
        return mark_safe(js)
