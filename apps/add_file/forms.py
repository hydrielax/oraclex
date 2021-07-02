from django import forms
from .widgets import SimpleFileInput


class ChoixFichiers(forms.Form):

    parameters = {'text': 'Sélectionner', 'multiple': True, 'upload_to': 'jugements'}
    fichiers = forms.FileField(label='', widget=SimpleFileInput(attrs=parameters))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id(self)
        self.fields['fichiers'].widget.form = self


class ConserverFichier(forms.Form):

    conserver = forms.BooleanField()
