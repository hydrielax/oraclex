from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ChoixFichiers, InfosJugement, TableauJugements
from .models import JugementTemp
from threading import Thread


@login_required
def ajout(request):
    if request.method == 'POST':
        fichiers = request.FILES.getlist('fichiers')
        for f in fichiers:
            jugement = JugementTemp(file=f)
            analyse = Thread(target=jugement.analyse)
            analyse.start()
    selection = ChoixFichiers()
    ajout.tableau = TableauJugements([])
    context = {'selection': selection, 'tableau': ajout.tableau}
    return render(request, 'add_file/index.html', context)
