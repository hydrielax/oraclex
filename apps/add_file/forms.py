from django import forms
from .widgets import CustomFileInput
from django.utils.safestring import mark_safe


class ChoixFichiers(forms.Form):

    parameters = {'multiple': True, 'upload_to': 'jugements'}
    fichiers = forms.FileField(label='', widget=CustomFileInput(attrs=parameters))


class Historique(list):

    def __str__(self):
        js = "[{name:'Nom du fichier', state:'État'}"
        for jugement in self:
            js += ", {{name:'{0}', state:'{1}'}}".format(jugement.name, type(jugement).__name__)
        js += "]"
        return mark_safe(js)
