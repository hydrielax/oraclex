from django import forms


class AjoutForm(forms.Form):
    fichiers = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'upload_to' : 'jugements'}))


class RecapFichier(forms.Form):
    conserver = forms.BooleanField()