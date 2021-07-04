from django import forms
from .widgets import SimpleFileInput
from apps.search.models import Jugement
from django.utils.html import format_html


class ChoixFichiers(forms.Form):

    parameters = {'text': 'Sélectionner', 'multiple': True, 'upload_to': 'jugements'}
    fichiers = forms.FileField(label='', widget=SimpleFileInput(attrs=parameters))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id(self)
        self.fields['fichiers'].widget.form = self


class InfosJugement(forms.Form):

    def __init__(self, fichier, **kwargs):
        super().__init__(**kwargs)
        self.jugement = Jugement.create(fichier)
        self.conserver = forms.BooleanField()


class TableauJugements(list):

    fields = ('nom', 'lisible', 'date_jugement', 'juridiction', 'gain')

    def sort(self, field, reverse):
        super().sort(key=lambda ligne: str(getattr(ligne.jugement, field)).lower(), reverse=reverse)

    def render(self, request):
        sort_field = request.GET.get('sort', 'nom')
        sort_reverse = request.GET.get('rv', 'n') == 'y'
        self.sort(sort_field, sort_reverse)
        html = ''
        if self:
            html += "<table class='table'><thead><tr>"
            for fld in self.fields:
                head = "<th><a href='?sort={field}&rv={rev}'>{name}{arrow}</a></th>"
                html += head.format(field=fld, rev='n' if sort_reverse else 'y',
                                    name=Jugement._meta.get_field(fld).verbose_name,
                                    arrow=(" &uarr;" if sort_reverse else " &darr;") if sort_field == fld else '')
            html += "<th><a href='javascript:void(0);'>Conserver</a></th>"
            html += "</tr></thead><tbody>"
            for lign in self:
                html += "<tr>"
                for fld in self.fields:
                    html += "<td>{}</td>".format(getattr(lign.jugement, fld))
                html += "<td>{}</td>".format(lign.conserver.widget.render('conserver', False))
                html += "</tr>"
            html += "</tbody></table>"
        return format_html(html)