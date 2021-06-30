from django import forms
from .widgets import SimpleFileInput


class AjoutForm(forms.Form):
    parameters = {'button_text': "Sélectionner", 'id': 'ajout', 'multiple': True, 'upload_to': 'jugements'}
    fichiers = forms.FileField(widget=SimpleFileInput(attrs=parameters))


class RecapFichier(forms.Form):
    conserver = forms.BooleanField()