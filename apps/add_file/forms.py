from django import forms
from django.forms.widgets import ClearableFileInput
from django.shortcuts import redirect
from unidecode import unidecode
from .analyse import find_keywords
from apps.search.models import Mot, MotCle


class ChoixFichiers(forms.Form):

    use_required_attribute = False
    options = {'upload_to': 'jugements', 'autocomplete': 'off', 'class': 'd-none', 'oninput': 'updateFileField();', 'multiple': True}
    fichiers = forms.FileField(label='', widget=ClearableFileInput(attrs={**options, 'accept': 'application/pdf'}))
    dossier = forms.FileField(label='', widget=ClearableFileInput(attrs={**options, 'webkitdirectory': True}))


class AjoutMotCleForm(forms.Form):
    mot_cle = forms.CharField(
        max_length=200,
        label = "Entrez un mot-clé à ajouter",
        help_text = "Tapez le mot-clé en majuscule, sans accents. Si le mot-clé peut s'écrire \
                    de plusieurs formes différentes, séparez les différentes \
                    formes avec des virgules. Ex : CDD, C.D.D., CONTRAT A \
                    DUREE DETERMINEE",
    )
    
    
    def __init__(self, *args, **kwargs):
        super(AjoutMotCleForm, self).__init__(*args, **kwargs)
        self.fields['mot_cle'].widget.attrs = {
            'class': 'form-control', 
            'placeholder': 'CONTRAT A DUREE DETERMINEE',
        }
    
    def verif(self, *args, **kwargs):
        mots = self.cleaned_data['mot_cle'].split(',')
        variantes = [unidecode(mot.strip().upper()) for mot in mots]
        for variante in variantes:
            if Mot.objects.filter(name=variante):
                return False
        return True
    
    def clean_mot_cle(self):
        mot_cle = self.cleaned_data['mot_cle']
        if not self.verif():
            from django.forms import ValidationError
            raise ValidationError('Le mot clé existe déjà')
        return mot_cle

    def save(self, *args, **kwargs):
        mots = self.cleaned_data['mot_cle'].split(',')
        variantes = [unidecode(mot.strip().upper()) for mot in mots]
        mot_principal = Mot(name = variantes[0])
        mot_principal.save()
        motcle = MotCle(representant = mot_principal)
        motcle.save()
        mot_principal.motcle = motcle
        mot_principal.save()
        for variante in variantes[1:]:
            mot = Mot(name = variante, motcle = motcle)
            mot.save()

