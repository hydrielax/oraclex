from django import forms
from django.forms import ModelForm, Form
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Agent

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
        }


class CreateUserForm(UserCreationForm, ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'password1': forms.PasswordInput(attrs={'class':'form-control'}),
            'password2': forms.PasswordInput(attrs={'class':'form-control'}),
        }


class AgentForm(ModelForm):
    class Meta:
        model = Agent
        fields = ['telephone']
        widgets = {
            'telephone': forms.TextInput(attrs={'class':'form-control'}),
        }


class RespoForm(Form):
    '''Formulaire de sélection d'un agent.'''
    
    respo = forms.ModelChoiceField(
        queryset=Agent.objects.all(),
        label="Choisir un responsable",
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tapez le nom d\'un utilisateur'}),
        required=False
    )