from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from apps.search.models import Jugement, Juridiction, MotCle, Responsable, TypeJuridiction, GroupeMotCle


@login_required
def infos(request):
    '''Génère les infos de la page Informations.'''

    # responsable
    respo = Responsable.objects.filter(id=1)
    if respo: respo = respo[0]

    # stats bdd
    num_jugements = Jugement.objects.count()
    num_lisibles = Jugement.objects.filter(lisible = True).count()
    num_illisibles = Jugement.objects.filter(lisible = False).count()

    # fichiers illisibles
    bad_files = Jugement.objects.filter(lisible = False).all()

    context = {
        'respo': respo,
        'num_jugements': num_jugements,
        'num_lisibles': num_lisibles,
        'num_illisibles': num_illisibles,
        'bad_files': bad_files,
    }
    return render(request, 'home/infos.html', context)




def responsable(request):
    '''Affiche le responsable de l'application en cours, même lorsqu'on
    n'est pas connecté.'''
    
    respo = Responsable.objects.get(id=1)
    context = {
        'respo': respo,
    }
    return render(request, 'infos/responsable.html', context=context) 