from django.db import models
from apps.search.models import BaseJugement, Jugement, MotCle
from threading import Thread
from .analyse import analyse


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thread = Thread(target=analyse, args=(self,), daemon=True)

    def register(self):
        fields = {fld.name: getattr(self, fld.name) for fld in BaseJugement._meta.fields}
        jugement = Jugement(**fields)
        jugement.save()
        jugement.mots_cles.set(self.mots_cles.all())
        self.delete()

    @classmethod
    def run_threads(cls, by=4):
        while True:
            jugements = cls.objects.all()[:by]
            for jugement in jugements:
                jugement.thread.start()
            for jugement in jugements:
                jugement.thread.join()


JugementTemp.thread = Thread(target=JugementTemp.run_threads, daemon=True)
