from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Agent


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
        }

class AgentForm(ModelForm):
    class Meta:
        model = Agent
        fields = ['telephone']
        widgets = {
            'telephone': forms.TextInput(attrs={'class':'form-control'}),
        }