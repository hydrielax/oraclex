from django import forms
from .widgets import CustomFileInput
from django.utils.safestring import mark_safe


class ChoixFichiers(forms.Form):

    parameters = {'multiple': True, 'upload_to': 'jugements'}
    fichiers = forms.FileField(label='', widget=CustomFileInput(attrs=parameters))


class Historique(list):

    def __str__(self):
        js = "[{date:`Date d'import`, name:'Nom du fichier', state:'État'}"
        for jugement in self:
            date = '<span order="{0}">{1}</span>'.format(jugement.date_import, jugement.date_import.strftime("%d/%m/%Y"))
            if (type(jugement).__name__ == 'Jugement'): state = '<span order="1" class="text-dark">Validé</span>'
            elif jugement.doublon: state = '<span order="2" class="text-red">Doublon ! Attente du responsable</span>'
            else: state = '<span order="3" class="text-success">En cours de traitement...</span>'
            js += ", {{date:'{0}', name:'{1}', state:'{2}'}}".format(date, jugement.name, state)
        js += "]"
        return mark_safe(js)
