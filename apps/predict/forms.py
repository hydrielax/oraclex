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
    
    type_juridiction = forms.ModelChoiceField(
        queryset=TypeJuridiction.objects.all(),
        label="Type de juridiction (peut etre à utiliser)",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    
    motsCles_textInput = forms.CharField(
        label="Mots-Clés",
        widget=forms.TextInput(attrs={'placeholder': 'Tapez les mots-clés séparés par une virgule', 'class': 'form-control'}),
        validators=[motscles_valide],
        required=False,
    )
    motsCles = forms.ModelMultipleChoiceField(
        queryset=MotCle.objects.all(),
        label="Mots-Clés (non-fonctionnel)",
        widget=MySelectMultiple(attrs={'class':"sr-only", 'id':"exampleFormControlMultiSelect3", 'data-role':"input", 'tabindex':"-1", 'aria-hidden':"true", 'multiple':'' }),
        # widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
