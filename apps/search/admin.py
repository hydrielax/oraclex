from django.contrib import admin
from .models import *


# page des mots-clés
class MotInline(admin.TabularInline):
    model = Mot

class MotCleAdmin(admin.ModelAdmin):
    inlines = [
        MotInline,
    ]
    list_display = ('__str__', 'categorie')
admin.site.register(MotCle, MotCleAdmin)

#autres pages standards
admin.site.register(TypeJuridiction)
admin.site.register(Categorie)


@admin.register(Juridiction)
class Juridiction(admin.ModelAdmin):
    list_display = ('nom', 'type_juridiction', 'ville')

@admin.register(Jugement)
class Jugement(admin.ModelAdmin):
    list_display = ('name', 'lisible', 'decision', 'gain', 'date_jugement', 'juridiction')
