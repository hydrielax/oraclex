from django.db import models
from django.urls import reverse
from datetime import date
from apps.add_file.conversion import *
import os
import random


class GroupeMotCle(models.Model):
    '''Objet représentant un groupe de mot-clé.'''
    nom = models.CharField('Groupe', max_length=50, unique=True)

    class Meta:
        ordering = ['nom']
        verbose_name = "Groupe de mots-clés"
        verbose_name_plural = "Groupes de mots-clés"

    def __str__(self):
        return self.nom


class MotCle(models.Model):
    '''Objet représentant un mot-clé. En plus du mot-clé principal, on peut ajouter des
       variantes de l'écriture du mot-clé pour la recherche dans les fichiers.'''
    nom = models.CharField('Mot-Clé', max_length=50, unique=True)
    variante1 = models.CharField('Variante 1', max_length=50, null=True, blank=True)
    variante2 = models.CharField('Variante 2', max_length=50, null=True, blank=True)
    variante3 = models.CharField('Variante 3', max_length=50, null=True, blank=True)
    groupe = models.ForeignKey('GroupeMotCle', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['groupe', 'nom']
        verbose_name = "Mot-clé"
        verbose_name_plural = "Mots-clés"

    def __str__(self):
        return self.nom



class TypeJuridiction(models.Model):
    '''Objet représentant un type de juridiction : Cour de Cassation, Appel, etc...'''
    cle = models.CharField('Abbréviation', max_length=2, primary_key=True)
    nom = models.CharField('Type', max_length=40)
    niveau = models.IntegerField('Niveau', help_text="Niveau de hiérarchie (1=première instance, 2 ensuite, etc...)")

    class Meta:
        ordering = ['niveau', 'nom']
        verbose_name = "Type de Juridiction"
        verbose_name_plural = "Types de Juridiction"

    def __str__(self):
        return self.nom



class Juridiction(models.Model):
    '''Objet représentant une juridiction.'''

    nom = models.CharField(max_length=70, null=True, blank=True)
    ville = models.CharField(max_length=40, null=True, blank=True)
    type_juridiction = models.ForeignKey('TypeJuridiction', to_field="cle", on_delete=models.SET_NULL, null=True, blank=True)
    rattachement = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'type_juridiction': 'CA'}, verbose_name='Cour de rattachement', help_text="Cour d'Appel de rattachement dans le cas d'un Conseil des Prud'Hommes")

    class Meta:
        ordering = ['type_juridiction', 'ville']

    def __str__(self):
        return self.nom



class Jugement(models.Model):
    '''Objet représentant un acte de jugement.'''
    file = models.FileField('Fichier', upload_to='jugements')
    nom = models.CharField('Nom du fichier', max_length=200, help_text='Nom du fichier')
    lisible = models.BooleanField('Lisible',help_text="Vrai si le fichier est lisible par l'ordinateur.")
    decision = models.CharField('Décision', max_length=1, choices=(('F', 'Favorable'), ('D', 'Défavorable'), ('M', 'Mixte')), null=True, blank=True, help_text='Décision de justice')
    date_jugement = models.DateField('Date du jugement', null=True, blank=True, help_text='Date du jugement')
    date_import = models.DateTimeField("Date d'import du jugement", auto_now_add=True)
    # juridiction = models.ForeignKey(Juridiction, on_delete=models.SET_NULL, null=True, blank=True, help_text='Cour ou Conseil du jugement')
    juridiction = models.ForeignKey(TypeJuridiction, verbose_name='Juridiction', on_delete=models.SET_NULL, null=True, blank=True, help_text='Cour ou Conseil du jugement')
    mots_cle = models.ManyToManyField(MotCle, verbose_name='Mot-Clé', help_text='Mots-clé présents dans le Jugement', blank=True)
    #gain = models.DecimalField(max_digits='10', decimal_places='2', help_text='Somme gagnée lors du procès (négative si perdu)', null=True, blank=True)
    gain = models.FloatField('Somme gangée', help_text='Somme gagnée lors du procès (négative si perdu)', null=True, blank=True)

    class Meta:
        ordering = ['-date_jugement']

    def __str__(self):
        return os.path.basename(self.file.name)

    def get_absolute_url(self):
        return reverse('jugement', args=[self.id])
    
    @classmethod
    def create(cls, f):
        jugement = cls(file=f, nom=f.name, lisible=random.choice([True, False]))
        return jugement





class Responsable(models.Model):
    '''Classe avec une seule instance, représentant le responsable en cours du site.
       À supprimer une fois que la classe Agent sera mise en place (avec une session par utilisateur,
       et une page pour modifier ses données.'''
    
    prenom = models.CharField('Prénom', max_length=50)
    nom = models.CharField('Nom', max_length=50)
    telephone = models.CharField('Téléphone', max_length=17)
    mail = models.EmailField('Email')
    en_charge = models.BooleanField(help_text='Vrai si le responsable est actuellement en charge.')

    class Meta:
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f'{self.prenom} {self.nom}'


