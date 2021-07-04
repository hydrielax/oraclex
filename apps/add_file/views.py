from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ChoixFichiers, InfosJugement, TableauJugements


@login_required
def ajout(request):
    if request.method == 'POST':
        fichiers = request.FILES.getlist('fichiers')
        ajout.tableau = TableauJugements([InfosJugement(f) for f in fichiers])
    if request.method == 'GET' and not request.GET.get('sort'):
            ajout.tableau = TableauJugements()
    selection = ChoixFichiers()
    context = {'selection': selection, 'tableau': ajout.tableau.render(request)}
    return render(request, 'add_file/index.html', context)