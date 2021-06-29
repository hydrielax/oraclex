from django.contrib import admin
from .models import *

#admin.site.register(Juridiction)
#admin.site.register(Jugement)
#admin.site.register(MotCle)
admin.site.register(TypeJuridiction)
admin.site.register(GroupeMotCle)
admin.site.register(Responsable)

@admin.register(Juridiction)
class Juridiction(admin.ModelAdmin):
    list_display = ('nom', 'type_juridiction', 'ville')

@admin.register(Jugement)
class Jugement(admin.ModelAdmin):
    list_display = ('__str__', 'lisible', 'decision', 'gain', 'date_jugement', 'juridiction')

@admin.register(MotCle)
class MotCle(admin.ModelAdmin):
    list_display = ('nom', 'groupe')
