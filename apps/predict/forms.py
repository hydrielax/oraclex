from django import forms
from apps.search.models import Mot
from apps.search.fields import ChipsWidget


class PredictForm(forms.Form):
    '''Formulaire de recherche.'''

    motcle = forms.MultipleChoiceField(
        choices = [],
        label = "Mots-clés",
        required=False,
        widget=ChipsWidget(attrs={'class': 'chips-input stretchy form-control', 'placeholder': 'Tapez un mot-clé'}),
        help_text = "Commencez à taper un mot-clé, sélectionnez-le dans la liste, puis tapez ENTREE pour le valider.",
    )

    def __init__(self, *args, **kwargs):
        super(PredictForm, self).__init__(*args, **kwargs)
        # this is pseudo code but you should get all variants
        # then get the product related to each variant
        self.fields['motcle'].choices = [(mot.name, mot.name) for mot in Mot.objects.all()]
