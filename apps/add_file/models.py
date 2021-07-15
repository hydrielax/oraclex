from django.db import models
from apps.search.models import BaseJugement, Jugement, MotCle


class JugementTemp(BaseJugement):

    doublon = models.ForeignKey(
        to = Jugement,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
    )

    class Meta:
        ordering = ['-date_import']
        verbose_name = 'Décision non validée'
        verbose_name_plural = 'Décisions non validées'

    def register(self):
        fields = {fld.name: getattr(self, fld.name) for fld in BaseJugement._meta.fields}
        jugement = Jugement(**fields)
        jugement.save()
        jugement.mots_cle.set(self.mots_cle.all())
        self.delete()