from django import forms
from django.forms.widgets import ClearableFileInput


class ChoixFichiers(forms.Form):

    use_required_attribute = False
    options = {'upload_to': 'jugements', 'autocomplete': 'off', 'class': 'd-none', 'oninput': 'updateFileField();', 'multiple': True}
    fichiers = forms.FileField(label='', widget=ClearableFileInput(attrs={**options, 'accept': 'application/pdf'}))
    dossier = forms.FileField(label='', widget=ClearableFileInput(attrs={**options, 'webkitdirectory': True}))

