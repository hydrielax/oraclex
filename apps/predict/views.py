
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.search.models import MotCle
from apps.search.recherche import find_motsCles
from .predict_model import model_ia
from .forms import PredictForm


@login_required
def prediction(request):
    context = {}

    if request.GET:
        form = PredictForm(request.GET)
        form.full_clean()
        if request.GET.getlist('motcle'):
            form.cleaned_data['motcle'] = request.GET.getlist('motcle')
            del form._errors['motcle']
        if form.is_valid():
            motsCles = find_motsCles(form.cleaned_data['motcle'])
            var_bool = [int(motCle in motsCles) for motCle in MotCle.objects.all()]
            proba = model_ia(var_bool)    #verify the form first
            context['proba'] = proba[0]
            context['dec'] = 'Def' if proba[0]>proba[1] else 'Fav'
            context['motsCles'] = motsCles
    else:
        form = PredictForm()

    context['form'] = form
    return render(request, 'predict/index.html', context)

