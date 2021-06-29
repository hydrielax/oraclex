from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('informations/', views.infos, name='infos'),
    path('responsable/', views.responsable, name='respo'),
]
