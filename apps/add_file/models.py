from django.db import models
from apps.search.models import BaseJugement, MotCle
from .analyse import extract_text, find_keywords, extract_date, extraction_somme


class JugementTemp(BaseJugement):

    file = models.FileField(
        verbose_name='Fichier',
        upload_to='jugements/temp'
    )
    doublon = models.ForeignKey(
        to = BaseJugement,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
    )

    class Meta:
        ordering = ['-date_import']
        verbose_name = 'Décision non validée'
        verbose_name_plural = 'Décisions non validées'

    def analyse(self):
        print('Start')
        text, quality = extract_text(self.file.file)
        mots_cle = find_keywords(text, MotCle.objects.all())
        somme = extraction_somme(text)
        date = extract_date(text)
        print(mots_cle, date, somme, text, quality)