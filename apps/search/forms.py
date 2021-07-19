from django import forms
from .models import Juridiction, TypeJuridiction, Jugement, MotCle, Categorie, Mot
from .fields import ListTextWidget, MySelectMultiple
import datetime

MONTHS = [('1','Janvier'), ('2','Février'), ('3','Mars'), ('4','Avril'), ('5','Mai'), ('6','Juin'), ('7','Juillet'), ('8','Août'), ('9','Septembre'), ('10','Octobre'), ('11','Novembre'), ('12','Décembre')]

class RequeteForm(forms.Form):
    '''Formulaire de recherche.'''

    datemMin = forms.ChoiceField(
        choices = MONTHS,
        label = "Date minimale - Mois",
        required=True,
        initial="1",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    dateyMin = forms.IntegerField(
        label = "Date minimale - Année",
        required=False,
        initial=1900,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value':1900}),
        min_value=1900,
        max_value=datetime.datetime.now().year,
    )
    datemMax = forms.ChoiceField(
        choices = MONTHS,
        label = "Date maximale - Mois",
        required=True,
        initial="8",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    dateyMax = forms.IntegerField(
        required=False,
        #initial=datetime.datetime.now().year,
        label = "Date maximale - Année",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value':datetime.datetime.now().year}),
        min_value=1900,
        max_value=datetime.datetime.now().year,
    )
    type_juridiction = forms.ModelChoiceField(
        queryset=TypeJuridiction.objects.all(),
        label="Type de juridiction",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )
    juridiction = forms.ModelChoiceField(
        queryset=Juridiction.objects.all(),
        label="Juridiction",
        # widget=forms.Select(attrs={'class': 'sr-only', 'id': "select3", 'data-role': "input", 'tabindex': "-1", 'aria-hidden': "true"}),
        widget=ListTextWidget(attrs={'class': 'form-control', 'placeholder': 'Tapez le nom de la ville'}),
        required=False
    )
    motcle = forms.ModelMultipleChoiceField(
        queryset=Mot.objects.all(),
        label = "Mots-clés",
        required=False,
    )
    # dateMin = forms.DateField(
    #     input_formats=["%Y %m"],
    #     label="Date Minimale",
    #     widget=forms.TextInput(attrs={'placeholder': 'AAAA MM', 'class': 'form-control'}),
    #     required=False
    # )
    # dateMax = forms.DateField(
    #     input_formats=["%Y %m"],
    #     label="Date Maximale",
    #     widget=forms.TextInput(attrs={'placeholder': 'AAAA MM', 'class': 'form-control'}),
    #     required=False
    # )
    # motsCles_textInput = forms.CharField(
    #     label="Mots-Clés",
    #     widget=forms.TextInput(attrs={'placeholder': 'Tapez les mots-clés séparés par une virgule', 'class': 'form-control'}),
    #     validators=[motscles_valide],
    #     required=False,
    # )
    # motsCles = forms.ModelMultipleChoiceField(
    #     queryset=MotCle.objects.all(),
    #     label="Mots-Clés (non-fonctionnel)",
    #     widget=MySelectMultiple(attrs={'class':"sr-only", 'id':"exampleFormControlMultiSelect3", 'data-role':"input", 'tabindex':"-1", 'aria-hidden':"true", 'multiple':'' }),
    #     # widget=forms.CheckboxSelectMultiple(),
    #     required=False,
    # )

