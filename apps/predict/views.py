
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from apps.predict.forms import RequeteForm
from apps.search.models import Jugement, MotCle, Categorie, Mot
from .predict_model import *




@login_required
def prediction(request):
    context = {}
    if request.method == 'POST':
        form = RequeteForm(request.POST)
        if form.is_valid():
            motsCles = form.cleaned_data['motsCles']
            #variantes = Mot.objects.filter(motcle__in=motsCles).values_list('name', flat=True)
            variantes = motsCles.values_list('representant__name', flat=True)
            var_bool = [int(motCle in motsCles) for motCle in MotCle.objects.all()]
            #proba = ia(variantes)
            proba = model_ia(var_bool)#verify the form first
            context['proba'] = proba
    else:
        form = RequeteForm()
    context['form'] = form
    return render(request, 'predict/index.html', context)


