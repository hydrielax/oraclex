from django import forms
from django.forms import ModelForm, Form
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Agent


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class':'form-control'}
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        # Labels
        self.fields['email'].label = "Adresse email"
        self.fields['first_name'].label = "Prénom"
        self.fields['last_name'].label = "Nom"
        # Helptexts
        self.fields['email'].help_text = "Requis. Entrez une adresse email valide."
        self.fields['first_name'].help_text = ""
        self.fields['last_name'].help_text = ""
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
            self.fields[field].widget.attrs = {'class':'form-control'}
    
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