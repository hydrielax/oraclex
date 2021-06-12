from django import forms
from .models import Juridiction, TypeJuridiction, Jugement, MotCle, GroupeMotCle
from .fields import ListTextWidget, MySelectMultiple


def motscles_valide(chaine):
    liste_motscles = [mot.nom.upper() for mot in MotCle.objects.all()]
    for mot in chaine.split(","):
        if (mot.strip().upper() not in liste_motscles):
            raise forms.ValidationError('Vous avez saisi un mot-clé incorrect')



class RequeteForm(forms.Form):
    '''Formulaire de recherche.'''
    dateMin = forms.DateField(
        input_formats=["%Y %m"],
        label="Date Minimale",
        widget=forms.TextInput(attrs={'placeholder': 'AAAA MM', 'class': 'form-control'}),
        required=False
    )
    dateMax = forms.DateField(
        input_formats=["%Y %m"],
        label="Date Maximale",
        widget=forms.TextInput(attrs={'placeholder': 'AAAA MM', 'class': 'form-control'}),
        required=False
    )
    type_juridiction = forms.ModelChoiceField(
        queryset=TypeJuridiction.objects.all(),
        label="Type de juridiction (non-fonctionnel)",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    juridiction = forms.ModelChoiceField(
        queryset=Juridiction.objects.all(),
        label="Juridiction",
        # widget=forms.Select(attrs={'class': 'sr-only', 'id': "select3", 'data-role': "input", 'tabindex': "-1", 'aria-hidden': "true"}),
        widget=ListTextWidget(attrs={'class': 'form-control', 'placeholder': 'Tapez le nom de la ville'}),
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


# Attention !!! Il y a déjà une classe Jugement pour stocker les fichiers !!!!

#class AjoutForm(forms.ModelForm):
    #class Meta  :
        #model = Document
        #fields = ('document',)
      
#
class AjoutForm(forms.Form):
    fichiers = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'upload_to' : 'jugements'}))


class RecapFichier(forms.Form):
    conserver = forms.BooleanField()