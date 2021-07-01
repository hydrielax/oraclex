from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import AjoutForm, RecapFichier
from apps.search.models import Jugement


@login_required
def ajouts(request):
    if request.method == 'POST':
        ajout = AjoutForm(request.POST, request.FILES)

        fichiers = request.FILES.getlist('fichiers')
        jugements = [Jugement.create(f) for f in fichiers]
        
        tableau = []
        for j in jugements:
            tableau.append(RecapFichier())
            tableau[-1].filename = j.file.name
            tableau[-1].lisible = j.lisible
            tableau[-1].date_jugement = j.date_jugement
            tableau[-1].juridiction = j.juridiction
            tableau[-1].gain = j.gain

        context = {
          'tableau': tableau,
          'ajout': ajout,
        }
    else:
        ajout = AjoutForm()
        context = {'ajout': ajout}
    return render(request, 'add_file/index.html', context)

