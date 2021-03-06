from django import forms
from .models import Juridiction, TypeJuridiction, Jugement, MotCle, Categorie, Mot
from .fields import ListTextWidget, MySelectMultiple, ChipsWidget
import datetime

MONTHS = [(1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'), (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'), (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')]

class RequeteForm(forms.Form):
    '''Formulaire de recherche.'''

    datemMin = forms.ChoiceField(
        choices = MONTHS,
        label = "Date minimale - Mois",
        required=True,
        initial=1,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    dateyMin = forms.IntegerField(
        label = "Date minimale - Année",
        required=False,
        initial=1900,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value':1900}),
        min_value=1900,
        max_value=datetime.date.today().year,
    )
    datemMax = forms.ChoiceField(
        choices = MONTHS,
        label = "Date maximale - Mois",
        required=True,
        initial=12,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    dateyMax = forms.IntegerField(
        required=False,
        #initial=datetime.datetime.now().year,
        label = "Date maximale - Année",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value':datetime.datetime.now().year}),
        min_value=1900,
        max_value=datetime.date.today().year,
    )
    type_juridiction = forms.ModelChoiceField(
        queryset=TypeJuridiction.objects.all(),
        label="Type de juridiction",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )
    juridiction = forms.ChoiceField(
        choices=[],
        label="Juridiction",
        # widget=forms.Select(attrs={'class': 'sr-only', 'id': "select3", 'data-role': "input", 'tabindex': "-1", 'aria-hidden': "true"}),
        widget=ListTextWidget(attrs={'class': 'form-control clear-option', 'placeholder': 'Tapez le nom de la ville', 'data-role':'input'}),
        required=False
    )
    motcle = forms.MultipleChoiceField(
        choices = [],
        label = "Mots-clés",
        required=False,
        widget=ChipsWidget(attrs={'class': 'chips-input stretchy form-control', 'placeholder': 'Tapez un mot-clé'}),
        help_text = "Commencez à taper un mot-clé, sélectionnez-le dans la liste, puis tapez ENTREE pour le valider.",
    )
    illisibles = forms.BooleanField(
        label = "Inclure les fichiers illsibles",
        widget = forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
        required = False,
    )

    def __init__(self, *args, **kwargs):
        super(RequeteForm, self).__init__(*args, **kwargs)
        # this is pseudo code but you should get all variants
        # then get the product related to each variant
        self.fields['motcle'].choices = [(mot.name, mot.name) for mot in Mot.objects.all()]
        self.fields['juridiction'].choices = [(j.nom, j.nom) for j in Juridiction.objects.all()]



class UpdateJugementForm(forms.ModelForm):
    delete = forms.ChoiceField(
        choices = (('-', '---------'), ('D', 'Supprimer')),
        required=False,
        label = "Supprimer la décision",
        help_text = "Cela supprimera cette décision de la base de données du site.",
    )
    class Meta:
        model = Jugement
        fields = ['date_jugement', 'juridiction', 'decision', 'gain', 'mots_cles', 'lisible']
    
    def __init__(self, *args, **kwargs):
        super(UpdateJugementForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
