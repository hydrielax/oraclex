from django import forms
from .widgets import SimpleFileInput, PersistentCheckbox
from apps.search.models import Jugement
from django.utils.safestring import mark_safe


class ChoixFichiers(forms.Form):

    parameters = {'text': 'Sélectionner', 'multiple': True, 'upload_to': 'jugements'}
    fichiers = forms.FileField(label='', widget=SimpleFileInput(attrs=parameters))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id(self)
        self.fields['fichiers'].widget.form = self


class InfosJugement(forms.Form):

    conserver = forms.BooleanField(widget=PersistentCheckbox())

    def __init__(self, fichier, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jugement = Jugement.create(fichier)
        self.conserver = self.fields['conserver']

    def __str__(self):
        js = "{{name:'{}', ".format(self.jugement.file.name)
        js += "lisible:'{}', ".format('Oui' if self.jugement.lisible else 'Non')
        js += "date:'{}', ".format(self.jugement.date_jugement)
        js += "juridiction:'{}', ".format(self.jugement.juridiction)
        js += "gain:'{}', ".format(self.jugement.gain)
        js += "conserver:`{}`}}".format(self.conserver.widget.render('checkbox', True))
        return mark_safe(js)


class TableauJugements(list):

    def __str__(self):
        js = "[{name:'Nom du fichier', lisible:'Lisible', date:'Date du jugement', " \
             "juridiction:'Juridiction', gain:'Somme gangée', conserver:'Conserver'}"
        js += "".join(", " + str(infos) for infos in self) + "]"
        return mark_safe(js)
