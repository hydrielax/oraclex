from django import forms
from django.forms import ModelForm, Form
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Agent


class UserForm(ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label="Prénom")
    last_name = forms.CharField(max_length=30, required=True, label="Nom")
    email = forms.EmailField(max_length=254, label="Adresse email", help_text='Requis. Entrez une adresse email valide.')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # Classes
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        #Placeholders
        self.fields['first_name'].widget.attrs['placeholder'] = 'Jean'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Dupont'
        self.fields['username'].widget.attrs['placeholder'] = 'jdupont'
        self.fields['email'].widget.attrs['placeholder'] = 'jean.dupont@sncf.fr'
        # Call to js
        self.fields['username'].widget.attrs['onclick'] = "create_username();"
        self.fields['username'].widget.attrs['onselect'] = "create_username();"
        # required
        self.fields['first_name'].widget.attrs['autofocus'] = 'True'
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Prénom")
    last_name = forms.CharField(max_length=30, required=True, label="Nom")
    email = forms.EmailField(max_length=254, label="Adresse email", help_text='Requis. Entrez une adresse email valide.')
    
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        # Classes
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        #Placeholders
        self.fields['first_name'].widget.attrs['placeholder'] = 'Jean'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Dupont'
        self.fields['username'].widget.attrs['placeholder'] = 'jdupont'
        self.fields['email'].widget.attrs['placeholder'] = 'jean.dupont@sncf.fr'
        # Call to js
        self.fields['username'].widget.attrs['onclick'] = "create_username();"
        self.fields['username'].widget.attrs['onselect'] = "create_username();"
        # required
        self.fields['first_name'].widget.attrs['autofocus'] = 'True'
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', )


class AgentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AgentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['telephone'].widget.attrs['placeholder'] = '06.04.05.03.02'
    
    class Meta:
        model = Agent
        fields = ['telephone']


class RespoForm(Form):
    '''Formulaire de sélection d'un agent.'''
    
    respo = forms.ModelChoiceField(
        queryset=Agent.objects.all(),
        label="Choisir un responsable",
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tapez le nom d\'un utilisateur'}),
        required=False
    )