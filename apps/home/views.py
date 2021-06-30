from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.search.models import Jugement, Responsable

@login_required
def home(request):
    '''Affiche la page d'accueil'''

    # responsable
    respo = Responsable.objects.filter(id=1)
    if respo: respo = respo[0]

    # stats bdd
    num_total = Jugement.objects.count()
    num_lisibles = Jugement.objects.filter(lisible = True).count()
    num_illisibles = Jugement.objects.filter(lisible = False).count()
    stats_bdd = {
        'total': num_total,
        'lisible': num_lisibles,
        'illisible': num_illisibles,
    }

    #envoi au template
    context = {
        'respo': respo,
        'stats_bdd': stats_bdd,
    }
    return render(request, 'home/home.html', context)


def responsable(request):
    '''Affiche le responsable de l'application en cours, même lorsqu'on
    n'est pas connecté.'''
    
    respos = Responsable.objects.all()
    if respos: 
        respo = respos[0]
    else:
        respo = None
    return render(request, 'home/responsable.html', context={'respo':respo}) 



def legal_mentions(request):
    '''Affiche les mentions légales'''

    respos = Responsable.objects.all()
    if respos: 
        respo = respos[0]
    else:
        respo = None
    return render(request, 'home/legal_mentions.html', context={'respo':respo})



def politics(request):
    '''Affiche la politique de confidentialité'''
    return render(request, 'home/politics.html') 

