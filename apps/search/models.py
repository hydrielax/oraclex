import os
from django.db import models
from django.urls import reverse
from apps.add_file.analyse import *
from apps.account.models import Agent


class MotCle(models.Model):
    '''Objet représentant un mot-clé. Un mot clé peut être rangé dans une catégorie.
       Il est aussi composé de plusieurs 'mots', qui constituent ses variantes.'''
    representant = models.ForeignKey(
        to = 'Mot', 
        on_delete = models.CASCADE, 
        related_name = 'representant_of',
    )
    categorie = models.ForeignKey(
        to = 'Categorie', 
        on_delete = models.SET_NULL, 
        null = True, 
        blank = True
    )

    class Meta:
        ordering = ['representant']
        verbose_name = "Mot-clé"
        verbose_name_plural = "Mots-clés"
    
    def __str__(self):
        return self.representant.name



class Categorie(models.Model):
    '''Objet représentant une catégorie de mots-clés afin de les ranger.'''
    name = models.CharField(
        verbose_name = 'Catégorie', 
        max_length = 50, 
        unique = True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name



class Mot(models.Model):
    '''Objet représentant un mot simple. Un mot-clé peut se référer à plusieurs mots simples.'''
    name = models.CharField(
        verbose_name = 'mot', 
        max_length=50,
        unique = True,
    )
    motcle = models.ForeignKey(
        to = MotCle, 
        on_delete = models.SET_NULL, 
        related_name = 'variantes',
        null = True,
        blank = True,
    )

    def __str__(self):
        return self.name
    


class TypeJuridiction(models.Model):
    '''Objet représentant un type de juridiction : Cour de Cassation, Appel, etc...'''
    cle = models.CharField(
        verbose_name = 'Abbréviation', 
        max_length = 2, 
        primary_key = True
    )
    nom = models.CharField(
        verbose_name = 'Type', 
        max_length = 40
    )
    niveau = models.IntegerField(
        verbose_name = 'Niveau', 
        help_text = "Niveau de hiérarchie (1=première instance, 2 ensuite, etc...)"
    )

    class Meta:
        ordering = ['niveau', 'nom']
        verbose_name = "Type de Juridiction"
        verbose_name_plural = "Types de Juridiction"

    def __str__(self):
        return self.nom



class Juridiction(models.Model):
    '''Objet représentant une juridiction.'''

    nom = models.CharField(
        max_length = 70, 
        null = True, 
        blank = True
    )
    ville = models.CharField(
        max_length = 40, 
        null = True, 
        blank = True
    )
    type_juridiction = models.ForeignKey(
        to = 'TypeJuridiction', 
        to_field = "cle", 
        on_delete = models.SET_NULL, 
        null = True, 
        blank = True
    )
    rattachement = models.ForeignKey(
        to = 'self', 
        on_delete = models.SET_NULL, 
        null = True, 
        blank = True, 
        limit_choices_to = {'type_juridiction': 'CA'}, 
        verbose_name = 'Cour de rattachement', 
        help_text = "Cour d'Appel de rattachement dans le cas d'un Conseil des Prud'Hommes"
    )

    class Meta:
        ordering = ['type_juridiction', 'ville']

    def __str__(self):
        return self.nom



class BaseJugement(models.Model):
    '''Objet représentant une décision de justice.'''
    file = models.FileField(
        verbose_name = 'Fichier',
        upload_to = 'jugements'
    )
    lisible = models.BooleanField(
        verbose_name = 'Lisible',
        help_text = "Vrai si le fichier est lisible par l'ordinateur.",
        null = True
    )
    decision = models.CharField(
        verbose_name = 'Décision', 
        max_length = 1, 
        choices = (('F', 'Favorable'), ('D', 'Défavorable'), ('M', 'Mixte')), 
        null = True, 
        blank = True, 
        help_text = 'Décision de justice'
    )
    date_jugement = models.DateField(
        verbose_name = 'Date du jugement', 
        null = True, 
        blank = True, 
        help_text = 'Date du jugement'
    )
    juridiction = models.ForeignKey(
        to = TypeJuridiction, 
        verbose_name = 'Juridiction', 
        on_delete = models.SET_NULL, 
        null = True, 
        blank = True, 
        help_text = 'Cour ou Conseil du jugement'
    )
    mots_cle = models.ManyToManyField(
        to = MotCle, 
        verbose_name = 'Mot-Clé', 
        help_text = 'Mots-clé présents dans le Jugement', 
        blank = True
    )
    gain = models.FloatField(
        verbose_name = 'Somme gagnée', 
        help_text = 'Somme gagnée lors du procès (négative si perdu)', 
        null = True, 
        blank = True
    )
    date_import = models.DateTimeField(
        verbose_name = "Date d'import du jugement", 
        auto_now_add = True
    )
    agent_import = models.ForeignKey(
        to = Agent,
        verbose_name = "Agent l'ayant importé",
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
    )

    class Meta:
        abstract = True

    @property
    def name(self):
        return os.path.basename(self.file.name)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('jugement', args=[self.id])


class Jugement(BaseJugement):

    class Meta:
        ordering = ['-date_jugement']
        verbose_name = 'Décision de justice'
        verbose_name_plural = 'Décisions de justice'
