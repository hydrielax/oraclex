from django.contrib import admin
from .models import JugementTemp


@admin.register(JugementTemp)
class JugementTemp(admin.ModelAdmin):
    list_display = ('name', 'doublon')
