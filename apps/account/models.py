from django.db import models
from django.contrib.auth.models import User


class Agent(models.Model):
    '''Extension de la classe user, pour remplacer la classe Reponsable à terme.'''
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField('Téléphone', max_length=17, null=True, blank=True)
    responsable = models.BooleanField(default=False, help_text='Vrai si le responsable est actuellement en charge.')
    
    @property
    def name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    def __str__(self):
        if self.name != ' ':
            return self.name
        else:
            return self.user.username

