from django import forms
from apps.search.models import Juridiction, TypeJuridiction, Jugement, MotCle, Categorie
from .fields import ListTextWidget, MySelectMultiple


def motscles_valide(chaine):
    liste_motscles = [mot.nom.upper() for mot in MotCle.objects.all()]
    for mot in chaine.split(","):
        if (mot.strip().upper() not in liste_motscles):
            raise forms.ValidationError('Vous avez saisi un mot-clé incorrect')



class RequeteForm(forms.Form):
    '''Formulaire de recherche.'''
    
    motsCles = forms.ModelMultipleChoiceField(
        queryset=MotCle.objects.all(),
        label="Mots-Clés",
        widget=forms.SelectMultiple(),
        required=False,
    )
