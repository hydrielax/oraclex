from django.db import models
from django.contrib.auth.models import User

class Agent(models.Model):
    '''Extension de la classe user, pour remplacer la classe Reponsable à terme.'''
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField('Téléphone', max_length=17)
    responsable = models.BooleanField(help_text='Vrai si le responsable est actuellement en charge.')

    class Meta:
        ordering = ['user']
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

