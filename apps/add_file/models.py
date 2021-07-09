from django.db import models
from apps.search.models import BaseJugement, MotCle
from .analyse import extract_text, find_keywords


class JugementTemp(BaseJugement):

    file = models.FileField(
        verbose_name='Fichier',
        upload_to='jugements/temp'
    )

    class Meta:
        ordering = ['-date_import']
        verbose_name = 'Décision non validée'
        verbose_name_plural = 'Décisions non validées'

    def analyse(self):
        print('Start')
        text, score = extract_text(self.file.file)
        mots_cle = find_keywords(text, MotCle.objects.all())
        print(mots_cle, text, score)