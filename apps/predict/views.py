
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from apps.predict.forms import RequeteForm
from apps.search.models import Jugement, MotCle, Categorie
from .predict_model import *




@login_required
def prediction(request):
    context = {}
    if request.method == 'POST':
        form = RequeteForm(request.POST)
        if form.is_valid():
            try:
                request.session['type_juridiction'] = form.cleaned_data['type_juridiction'].nom
            except:
                request.session['type_juridiction'] = None
            motsCles = list(set([mot.nom for mot in form.cleaned_data['motsCles']] + [m.upper() for m in form.cleaned_data['motsCles_textInput'].split(",")]))
            #motsCles.remove('')
            request.session['motsCles'] = motsCles
            return redirect('predict:resultat_predict')
    else:
        form = RequeteForm()

    indexmotcles = MotCle.objects.all()
    groupes = Categorie.objects.all()
    liste = []
    for i in range(0, len(groupes)):
        listeMotCle = []
        mots_cles = MotCle.objects.filter(groupe=groupes[i])
        for motcle in mots_cles:
            index=0
            #while indexmotcles[index]!=motcle: index+=1
            listeMotCle.append({'id': motcle.id, 'nom': motcle.representant.name, })
        liste.append({'id':i, 'nom': groupes[i].nom, 'mots_cles': listeMotCle, })
    
    #en 2 : mots-clés sans groupes
    liste2 = []
    mots_cles = MotCle.objects.filter(categorie__isnull=True)
    for motcle in mots_cles:
        index=0
        #while indexmotcles[index]!=motcle: index+=1
        liste2.append({'id': motcle.id, 'nom': motcle.representant.name, })

    context = {
        'form': form, 
        'liste': liste,
        'liste_sans_groupe': liste2,
    }
    return render(request, 'predict/index.html', context)



@login_required
def resultat_predict(request): #resultat_predict au lieu de resultat
    # recuperation des donnees saisies
    type_juridiction = request.session['type_juridiction']
    motsCles = request.session['motsCles']

    parametres = {
        
        'motsCles': motsCles,

        'type_juridiction': type_juridiction,
    }

    # graphiques
    

    return render(request, 'search/resultat_predict.html', {
        'parametres': parametres,
        
        # à ajouter
    })
